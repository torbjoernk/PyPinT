# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from collections.abc import Sequence
from weakref import ref, ReferenceType
from copy import deepcopy

from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.solutions.i_solution import ISolution
from pypint.utilities.states.node_state import NodeState
from pypint.utilities.assertions import assert_condition, assert_is_instance, assert_named_argument
from pypint.utilities.tracing import class_name
from pypint.utilities.abc import Deepcopyable
from pypint.utilities.logging import LOG


class StateSequence(Sequence, Deepcopyable):
    """Specialized sequence of states with fixed number of states.
    """

    def __init__(self, **kwargs):
        assert_named_argument('solution_type', kwargs, types=(list, type), descriptor="Solution Type",
                              checking_obj=self)
        if isinstance(kwargs['solution_type'], list):
            assert_condition(issubclass(kwargs['solution_type'][0], (ISolution, TrajectorySolutionData)),
                             ValueError,
                             message="Solution Data Type must be a subclass of ISolution or TrajectorySolutionData: "
                                     "NOT %s" % kwargs['solution_type'][0].__name__,
                             checking_obj=self)
        else:
            assert_condition(issubclass(kwargs['solution_type'], (ISolution, TrajectorySolutionData)),
                             ValueError,
                             message="Solution Data Type must be a subclass of ISolution or TrajectorySolutionData: "
                                     "NOT %s" % kwargs['solution_type'].__name__,
                             checking_obj=self)

        assert_named_argument('element_type', kwargs, types=(list, type), descriptor="Element Type", checking_obj=self)
        if isinstance(kwargs['element_type'], list):
            assert_condition(issubclass(kwargs['element_type'][0], (NodeState, StateSequence)),
                             ValueError,
                             message="Element Data Type must be a subclass of NodeState or MutableStateSequence: "
                                     "NOT %s" % kwargs['element_type'][0].__name__,
                             checking_obj=self)
        else:
            assert_condition(issubclass(kwargs['element_type'], (NodeState, StateSequence)),
                             ValueError,
                             message="Element Data Type must be a subclass of NodeState or MutableStateSequence: "
                                     "NOT %s" % kwargs['element_type'].__name__,
                             checking_obj=self)

        assert_named_argument('num_states', kwargs, types=(list, int), descriptor="Number of States", checking_obj=self)
        if isinstance(kwargs['num_states'], list):
            assert_condition(kwargs['num_states'][0] >= 0,
                             ValueError, message="Number of States must be positive: NOT %d" % kwargs['num_states'][0],
                             checking_obj=self)
        else:
            assert_condition(kwargs['num_states'] >= 0,
                             ValueError, message="Number of States must be positive: NOT %d" % kwargs['num_states'],
                             checking_obj=self)

        if isinstance(kwargs['solution_type'], list):
            self._solution = kwargs['solution_type'][0]()
            del kwargs['solution_type'][0]
            if len(kwargs['solution_type']) == 0:
                del kwargs['solution_type']
        else:
            self._solution = kwargs['solution_type']()
            del kwargs['solution_type']

        if isinstance(kwargs['element_type'], list):
            self._element_type = kwargs['element_type'][0]
            del kwargs['element_type'][0]
            if len(kwargs['element_type']) == 0:
                del kwargs['element_type']
        else:
            self._element_type = kwargs['element_type']
            del kwargs['element_type']

        self._parent = None
        self._states = []
        self._current_index = 0
        self._finalized = False

        if isinstance(kwargs['num_states'], list):
            _num_states = kwargs['num_states'][0]
            del kwargs['num_states'][0]
            if len(kwargs['num_states']) == 0:
                del kwargs['num_states']
        else:
            _num_states = kwargs['num_states']
            del kwargs['num_states']
        for _ in range(0, _num_states):
            _kwargs = deepcopy(kwargs)
            self._add_state(self._element_type(**_kwargs))

    def finalize(self):
        """Finalize this sequence of states

        This copies the solution data from all containing states to its own solution object and finalizes it.
        As well, the :py:attr:`.current_index` is reset to zero.

        Raises
        ------
        RuntimeError
            If this state has already been finalized.
        """
        assert_condition(not self.finalized, RuntimeError,
                         message="This %s is already finalized." % class_name(self), checking_obj=self)
        for _state in self:
            _state.finalize()
            self.solution.add_solution_data(deepcopy(_state.solution))
        self.solution.finalize()
        self.reset_current_index()
        self._finalized = True

    def reset_current_index(self):
        """Resets the current index state to the start of this sequence
        """
        self._current_index = 0

    def proceed(self):
        """Proceeds :py:attr:`.current` to the next state in the sequence

        Raises
        ------
        RuntimeError
            if this sequence has already been finalized via :py:meth:`.MutableStateSequence.finalize`
        """
        assert_condition(not self.finalized, RuntimeError,
                         message="This {} is already done.".format(class_name(self)),
                         checking_obj=self)
        if self.next_index is not None:
            self._current_index += 1
        else:
            raise StopIteration("No further states available.")

    def broadcast(self, value):
        for _step in self:
            _step.value = deepcopy(value)

    @property
    def parent(self):
        if self._parent is not None:
            return self._parent()
        else:
            return None

    @parent.setter
    def parent(self, value):
        assert_is_instance(value, ReferenceType, descriptor="Parent Container", checking_obj=self)
        self._parent = value

    @property
    def previous_sibling(self):
        if self.parent:
            if self.parent.index(self) - 1 >= 0:
                return self.parent[self.parent.index(self) - 1]
            else:
                return None
        else:
            # no parent given
            return None

    @property
    def next_sibling(self):
        if self.parent:
            if self.parent.index(self) + 1 < len(self.parent):
                return self.parent[self.parent.index(self) + 1]
            else:
                return None
        else:
            # no parent given
            return None

    @property
    def finalized(self):
        """Read-only accessor to determine the finalized state of this state sequence

        Raises
        ------
        RuntimeError
            if this object is finalized but its containing solution object is not
            (though, this should never happen)
        """
        if self._finalized:
            # if this throws, something is really broken
            assert_condition(self.solution.finalized, RuntimeError,
                             message="State is finalized but not its solution object. (something is really broken!)",
                             checking_obj=self)
        return self._finalized

    @property
    def solution(self):
        """Accessor for the containing solution object
        """
        return self._solution

    @property
    def current(self):
        """Accessor to the current state of this sequence
        """
        return self[self.current_index] if self.current_index is not None else None

    @property
    def current_index(self):
        """Index of the current state of this sequence
        """
        return self._current_index if len(self) > self._current_index else None

    @property
    def previous(self):
        """Accessor to the previous state of this sequence

        Returns
        -------
        previous : :py:class:`.NodeState`, :py:class:`.MutableStateSequence` or :py:class:`None`
            :py:class:`None` if :py:attr:`.previous_index` returns :py:class:`None`
        """
        return self[self.previous_index] if self.previous_index is not None else None

    @property
    def previous_index(self):
        """Index of the previous state of this sequence

        Returns
        -------
        previous_index : :py:class:`int` or :py:class:`None`
            :py:class:`None` if no previous state is available, i.e. if :py:attr:`.current_index` is 0
        """
        return self.current_index - 1 if self.current_index is not None and self.current_index > 0 else None

    @property
    def next(self):
        """Accessor for the next state in this sequence

        Returns
        -------
        next : :py:class:`.NodeState`, :py:class:`.MutableStateSequence` or :py:class:`None`
            :py:class:`None` if :py:attr:`.next_index` is :py:class:`None`
        """
        return self[self.next_index] if self.next_index is not None else None

    @property
    def next_index(self):
        """Index of the next state in this sequence

        Returns
        -------
        next_index : :py:class:`int` or :py:class:`None`
            :py:class:`None` if :py:attr:`.current` is already the last state in this sequence
        """
        return self.current_index + 1 \
            if self.current_index is not None and len(self) > self.current_index + 1 else None

    @property
    def first(self):
        """Accessor to the first state of this sequence

        Returns
        -------
        first : :py:class:`None`
            if :py:attr:`.first_index` returns :py:class:`None`
        """
        return self[self.first_index] if self.first_index is not None else None

    @property
    def first_index(self):
        """Index of the first state of this seuqence

        Returns
        -------
        first_index : ``0`` or :py:class:`None`
            :py:class:`None` is returned, if there are no states in this sequence
        """
        return 0 if len(self) > 0 else None

    @property
    def last(self):
        """Accessor for the last state in this sequence

        Returns
        -------
        last : :py:class:`.NodeState`, :py:class:`.MutableStateSequence` or :py:class:`None`
            :py:class:`None` if :py:attr:`.last_index` is :py:class:`None`
        """
        return self[self.last_index] if self.last_index is not None else None

    @property
    def last_index(self):
        """Index of the last state in this sequence

        Returns
        -------
        last_index : :py:class:`int` or :py:class:`None`
            :py:class:`None` if there are no states in this sequence
        """
        return len(self) - 1 if len(self) > 0 else None

    def _add_state(self, state):
        self._states.append(state)
        state.parent = ref(self)

    def __len__(self):
        return len(self._states)

    def __getitem__(self, item):
        return self._states[item]

    def __str__(self):
        return "%s<0x%x>(size=%d)" % (class_name(self), id(self), len(self))

    def __repr__(self):
        return "<%s at 0x%x : size=%d>" % (class_name(self), id(self), len(self))


__all__ = ['StateSequence']
