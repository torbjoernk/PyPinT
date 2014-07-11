# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from abc import ABCMeta, abstractmethod

from pypint.integrators.abstract_integrator import AbstractIntegrator
from pypint.problems.has_exact_solution_mixin import problem_has_exact_solution
from pypint.problems.i_problem import IProblem
from pypint.solvers.diagnosis import Error, Residual
from pypint.utilities.assertions import assert_named_argument


class AbstractSdc(AbstractIntegrator, metaclass=ABCMeta):
    """Provides the Step-Method-Core for :py:class:`.Sdc` solver.

    This is to be used as a Mixin for the :py:class:`.Sdc` solver to provide the core step-methods such as the explicit,
    implicit and semi-implicit Euler.

    Notes
    -----
    The scope of `self` must be seen in the context of a :py:class:`.Sdc` solver instance here.
    Thus, access to :py:attr:`.Sdc.problem` or :py:attr:`.Sdc.is_implicit` is perfectly fine (though IDEs will not
    resolve this correctly).

    As well, note, that :py:meth:`.SdcCoreMixin.__init__` must be called explicitly and is not called via
    :py:func:`super` calls.
    :py:meth:`.SdcCoreMixin.__init__` is called by :py:meth:`.Sdc.init`.
    """

    def __init__(self, *args, **kwargs):
        super(AbstractSdc, self).__init__(*args, **kwargs)

    @abstractmethod
    def run(self, state, **kwargs):
        super(AbstractSdc, self).run(state, **kwargs)

    def compute_residual(self, state, **kwargs):
        # LOG.debug("computing residual")
        super(AbstractSdc, self).compute_residual(state, **kwargs)
        _step = kwargs['step'] if 'step' in kwargs else state.current_step
        _step.solution.residual = Residual(
            abs(state.current_time_step.initial.value
                + state.delta_interval * kwargs['integral']
                - _step.value)
        )
        # LOG.debug("Residual: {: .4f} = | {: .4f} + {: .4f} * {: .4f} - {: .4f} |"
        #           .format(state.current_step.solution.residual.value[0],
        #                   state.current_time_step.initial.value[0],
        #                   state.delta_interval, kwargs['integral'][0],
        #                   state.current_step.value[0]))

    def compute_error(self, state, **kwargs):
        super(AbstractSdc, self).compute_error(state, **kwargs)

        assert_named_argument('problem', kwargs, types=IProblem, descriptor="Problem", checking_obj=self)

        _problem = kwargs['problem']

        if problem_has_exact_solution(_problem, self):
            # LOG.debug("Error for t={:.3f}: {} - {}".format(state.current_step.time_point,
            #                                               state.current_step.value,
            #                                               _problem.exact(state.current_step.time_point)))
            state.current_step.solution.error = Error(
                abs(state.current_step.value - _problem.exact(state.current_step.time_point))
            )
        else:
            # we need the exact solution for that
            #  (unless we find an error approximation method)
            pass

    @AbstractIntegrator.name.getter
    @abstractmethod
    def name(self):
        super(self.__class__, self.__class__).name.fget(self)
        return 'SDC Integrator Interface'

    def _previous_iteration_previous_step(self, state):
        if state.previous_iteration_index is not None:
            if state.previous_step_index is not None:
                return state.previous_iteration[state.current_time_step_index][state.previous_step_index]
            else:
                return state.previous_iteration[state.current_time_step_index].initial
        else:
            return state.initial

    def _previous_iteration_current_step(self, state):
        if state.previous_iteration_index is not None:
            return state.previous_iteration[state.current_time_step_index][state.current_step_index]
        else:
            return state.initial


__all__ = ['AbstractSdc']
