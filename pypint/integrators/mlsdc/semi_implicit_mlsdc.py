# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.kaltt@fz-juelich.de>
"""
import numpy as np

from integrators.mlsdc.mlsdc_integrator import MlSdcIntegrator
from pypint.solvers.states.mlsdc_solver_state import MlSdcSolverState
from pypint.problems.i_problem import IProblem
from pypint.problems.has_direct_implicit_mixin import problem_has_direct_implicit
from pypint.utilities.assertions import assert_is_instance, assert_named_argument
from pypint.utilities.logging import LOG


class SemiImplicitMlSdc(MlSdcIntegrator):
    """Semi-Implicit MLSDC Core
    """

    name = "Semi-Implicit SDC"

    def __init__(self):
        super(SemiImplicitMlSdc, self).__init__()

    def run(self, state, **kwargs):
        """Semi-Implicit Euler step method.

        .. math::

            u_{m+1}^{k+1} - \\Delta_\\tau F_I(t_{m+1}, u_{m+1}^{k+1}) =
                u_m^{k+1} &+ \\Delta_\\tau \\left( F_I(t_{m+1}, u_{m+1}^k)
                                                  - F_E(t_m, u_m^{k+1}) + F_E(t_m, u_m^k) \\right) \\\\
                          &+ \\Delta_t I_m^{m+1} \\left( F(\\vec{u}^k) \\right)

        Parameters
        ----------
        state : :py:class:`.MlSdcSolverState`

        Notes
        -----
        This step method requires the given problem to provide partial evaluation of the right-hand side.
        """
        super(SemiImplicitMlSdc, self).run(state, **kwargs)

        assert_is_instance(state, MlSdcSolverState, descriptor="State", checking_obj=self)
        assert_named_argument('problem', kwargs, types=IProblem, descriptor="Problem", checking_obj=self)
        _problem = kwargs['problem']

        use_intermediate = kwargs['use_intermediate'] if 'use_intermediate' in kwargs else False

        if use_intermediate:
            # LOG.debug("using intermediate")
            _previous_iteration_current_step = state.current_iteration.current_level.current_step.intermediate
        elif not state.current_iteration.on_finest_level:
            _previous_iteration_current_step = state.current_iteration.current_level.current_step
        else:
            _previous_iteration_current_step = self._previous_iteration_current_step(state)
        if not _previous_iteration_current_step.rhs_evaluated:
            _previous_iteration_current_step.rhs = \
                _problem.evaluate_wrt_time(_previous_iteration_current_step.time_point,
                                           _previous_iteration_current_step.value)

        if not state.current_iteration.on_finest_level:
            _previous_iteration_previous_step = state.current_iteration.current_level.previous_step
        else:
            _previous_iteration_previous_step = self._previous_iteration_previous_step(state)
        if not _previous_iteration_previous_step.rhs_evaluated:
            _previous_iteration_previous_step.rhs = \
                _problem.evaluate_wrt_time(_previous_iteration_previous_step.time_point,
                                           _previous_iteration_previous_step.value)

        _fas = np.zeros(_previous_iteration_current_step.rhs.shape,
                        dtype=_previous_iteration_current_step.rhs.dtype)
        if not use_intermediate and _previous_iteration_current_step.has_fas_correction():
            # LOG.debug("   previous iteration current step has FAS: %s"
            #           % _previous_iteration_current_step.fas_correction)
            _fas = _previous_iteration_current_step.fas_correction

        if problem_has_direct_implicit(_problem, self):
            _sol = _problem.direct_implicit(phis_of_time=[_previous_iteration_previous_step.value,
                                                          _previous_iteration_current_step.value,
                                                          state.previous_step.value],
                                            delta_node=state.current_step.delta_tau,
                                            delta_step=state.delta_interval,
                                            integral=state.current_step.integral,
                                            fas=_fas,
                                            core=self)

        else:
            # Note: \Delta_t is always 1.0 as it's part of the integral
            _Fe_u_cp = _problem.evaluate_wrt_time(state.previous_step.time_point,
                                               state.previous_step.value,
                                               partial="expl")
            _Fe_u_pp = _problem.evaluate_wrt_time(_previous_iteration_previous_step.time_point,
                                                 _previous_iteration_previous_step.value,
                                                 partial="expl")
            _Fe_u_pc = _problem.evaluate_wrt_time(state.current_step.time_point,
                                                 _previous_iteration_current_step.value,
                                                 partial="impl")
            _expl_term = \
                (state.previous_step.value
                 + state.current_step.delta_tau
                 * (_Fe_u_cp - _Fe_u_pp - _Fe_u_pc)
                 + state.current_step.integral + _fas).reshape(-1)
            # LOG.debug("EXPL TERM: %s = %s + %f * (%s - %s - %s) + %s + %s"
            #           % (_expl_term, state.previous_step.value, state.current_step.delta_tau, _Fe_u_cp, _Fe_u_pp,
            #              _Fe_u_pc, state.current_step.integral, _fas))
            _func = lambda x_next: \
                _expl_term \
                + state.current_step.delta_tau * _problem.evaluate_wrt_time(state.current_step.time_point,
                                                                            x_next.reshape(_problem.dim_for_time_solver),
                                                                            partial="impl").reshape(-1) \
                - x_next
            # LOG.debug("shape of value: %s" % (state.current_step.value.shape,))
            # LOG.debug("shape expl term: %s" % (_expl_term.shape,))
            # LOG.debug("shape impl func: %s" % (_func(state.current_step.value.reshape(-1)).shape,))
            _sol = \
                _problem.implicit_solve(
                    state.current_step.value.reshape(-1),
                    _func,
                    expl_term=_expl_term,
                    time_level=state.current_iteration.current_level_index,
                    delta_time=state.current_iteration.current_level.current_step.delta_tau
                ).reshape(state.current_step.value.shape)

        if type(state.current_step.value) == type(_sol):
            state.current_step.value = _sol
        else:
            LOG.debug("Solution Type %s but expected %s" % (type(_sol), type(state.current_step.value)))
            state.current_step.value = _sol[0]


__all__ = ['SemiImplicitMlSdc']
