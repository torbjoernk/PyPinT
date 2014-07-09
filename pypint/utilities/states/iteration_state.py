# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from copy import deepcopy

from pypint.utilities.states.mutable_state_sequence import MutableStateSequence
from pypint.solutions.iterative_solution import IterativeSolution
from pypint.utilities.tracing import class_name
from pypint.utilities.assertions import assert_condition, assert_is_instance


class IterationState(MutableStateSequence):
    """Stores states of a single iteration.
    """
    def __init__(self, **kwargs):
        super(IterationState, self).__init__(**kwargs)
        assert_is_instance(self._solution, IterativeSolution, descriptor="Solution", checking_obj=self)
        self._element_args = deepcopy(kwargs)
        self.append(self._element_type(**deepcopy(self._element_args)))

    def proceed(self):
        self.append(self._element_type(**deepcopy(self._element_args)))
        super(IterationState, self).proceed()

    def finalize(self):
        """Finalizes this iteration and copies solutions

        The solutions of all steps of all time steps are copied to this sequence's :py:class:`.TrajectorySolutionData`
        and is finalized afterwards.

        The remaining behaviour is the same as the overridden method.

        See Also
        --------
        :py:meth:`.MutableStateSequence.finalize` : overridden method
        """
        assert_condition(not self.finalized, RuntimeError,
                         message="This {} is already done.".format(class_name(self)),
                         checking_obj=self)
        for _state in self:
            _state.finalize()
            self.solution.add_solution(deepcopy(_state.solution))
        self.solution.finalize()
        self._current_index = 0
        self._finalized = True


__all__ = ['IterationState']
