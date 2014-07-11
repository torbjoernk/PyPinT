# coding=utf-8
"""

.. moduleauthor:: Torbjörn Klatt <t.kaltt@fz-juelich.de>
"""
from pypint.integrators.sdc.abstract_sdc import AbstractSdc
from pypint.utilities.states.sdc_solver_state import SdcSolverState
from pypint.problems.i_problem import IProblem
from pypint.utilities.assertions import assert_is_instance, assert_named_argument


class ExplicitSdc(AbstractSdc):
    """Explicit SDC Core
    """

    def __init__(self, *args, **kwargs):
        super(ExplicitSdc, self).__init__(*args, **kwargs)

    def run(self, state, **kwargs):
        """Explicit Euler step method.

        .. math::

            u_{m+1}^{k+1} = u_m^{k+1} + \\Delta_\\tau \\left( F(t_m, u_m^{k+1}) - F(t_m, u_m^k) \\right)
                                      + \\Delta_t I_m^{m+1} \\left( F(\\vec{u}^k) \\right)

        Parameters
        ----------
        solver_state : :py:class:`.SdcSolverState`
        """
        super(ExplicitSdc, self).run(state, **kwargs)

        assert_is_instance(state, SdcSolverState, descriptor="State", checking_obj=self)
        assert_named_argument('problem', kwargs, types=IProblem, descriptor="Problem", checking_obj=self)

        _problem = kwargs['problem']

        _previous_step = state.previous_step
        _previous_iteration_previous_step = self._previous_iteration_previous_step(state)

        if not _previous_step.rhs_evaluated:
            _previous_step.rhs = _problem.evaluate_wrt_time(state.current_step.time_point, _previous_step.value)
        if not _previous_iteration_previous_step.rhs_evaluated:
            _previous_iteration_previous_step.rhs = \
                _problem.evaluate_wrt_time(state.current_step.time_point, _previous_iteration_previous_step.value)

        # using step-wise formula
        # Formula:
        #   u_{m+1}^{k+1} = u_m^{k+1} + \Delta_\tau [ F(u_m^{k+1}) - F(u_m^k) ] + \Delta_t I_m^{m+1}(F(u^k))
        # Note: \Delta_t is always 1.0 as it's part of the integral
        state.current_step.value = \
            (_previous_step.value + state.current_step.delta_tau
             * (_previous_step.rhs - _previous_iteration_previous_step.rhs)
             + state.current_step.integral)

    @AbstractSdc.name.getter
    def name(self):
        super(self.__class__, self.__class__).name.fget(self)
        return 'Explicit SDC Integrator'


__all__ = ['ExplicitSdc']
