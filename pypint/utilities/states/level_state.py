# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from copy import deepcopy

from pypint.utilities.states.iteration_state import IterationState
from pypint.utilities.states.timestep_state import TimeStepState
from pypint.utilities.states.node_state import NodeState


class LevelState(IterationState):
    def __init__(self, **kwargs):
        if 'element_type' not in kwargs:
            kwargs['element_type'] = [TimeStepState, NodeState]
        super(LevelState, self).__init__(**kwargs)
        self._intermediate = None

    @property
    def intermediate(self):
        return self._intermediate

    @intermediate.setter
    def intermediate(self, value):
        self._intermediate = value

    def reset_intermediate(self):
        self._intermediate = self._element_type(**deepcopy(self._element_args))


__all__ = ['LevelState']
