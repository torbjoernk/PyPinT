# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from collections.abc import MutableSequence
from weakref import ref

from pypint.utilities.states.node_state import NodeState
from pypint.utilities.states.state_sequence import StateSequence
from pypint.utilities.assertions import assert_is_instance


class MutableStateSequence(StateSequence, MutableSequence):
    """Interface for a mutable sequence of states.

    In addition to :py:class:`.StateSequence`, :py:class:`.MutableStateSequence` models a mutable sequence of states
    allowing for easy addition (:py:meth:`append` and :py:meth:`insert`) and deletion (:py:meth:`del`) of states.
    """
    def __init__(self, **kwargs):
        """
        See :py:meth:`.StateSequence.__init__` where ``num_states`` defaults to 0 if not given.
        """
        if 'num_states' not in kwargs:
            kwargs['num_states'] = 0
        super(MutableStateSequence, self).__init__(**kwargs)

    def insert(self, index, item):
        assert_is_instance(item, (NodeState, StateSequence), descriptor="State Sequence Item",
                           checking_obj=self)
        self._states.insert(index, item)

    def __setitem__(self, index, item):
        assert_is_instance(item, (NodeState, StateSequence), descriptor="State Sequence Item",
                           checking_obj=self)
        self._states[index] = item
        item.parent = ref(self)

    def __delitem__(self, index):
        if 0 <= abs(index) < len(self):
            del self._states[index]
        else:
            raise IndexError


__all__ = ['MutableStateSequence']
