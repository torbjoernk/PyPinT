# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np

from pypint.utilities.states.solver_state import SolverState
from pypint.utilities.states.level_state import LevelState
from pypint.utilities.states.timestep_state import TimeStepState
from pypint.utilities.states.node_state import NodeState
from pypint.solutions.final_solution import FinalSolution
from pypint.solutions.iterative_solution import IterativeSolution
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.utilities.assertions import assert_condition, assert_named_argument


class MlSdcNodeState(NodeState):
    def __init__(self, **kwargs):
        super(MlSdcNodeState, self).__init__(**kwargs)
        self._fas_correction = None
        self._coarse_correction = 0.0
        self._intermediate = NodeState()

    def has_fas_correction(self):
        return self._fas_correction is not None

    @property
    def intermediate(self):
        return self._intermediate

    @property
    def coarse_correction(self):
        return self._coarse_correction

    @coarse_correction.setter
    def coarse_correction(self, coarse_correction):
        self._coarse_correction = coarse_correction

    @property
    def fas_correction(self):
        return self._fas_correction

    @fas_correction.setter
    def fas_correction(self, fas_correction):
        if not isinstance(fas_correction, np.ndarray):
            # LOG.debug("FAS Correction not given as Array. Converting it to one.")
            fas_correction = np.array([fas_correction])
        self._fas_correction = fas_correction


class MlSdcLevelState(LevelState):
    def __init__(self, **kwargs):
        kwargs['solution_class'] = TrajectorySolutionData
        kwargs['element_type'] = MlSdcNodeState
        super(MlSdcLevelState, self).__init__(**kwargs)

        self._initial = MlSdcNodeState()
        self._integral = 0.0

    @property
    def initial(self):
        """Accessor for the initial value of this time step
        """
        return self._initial

    @initial.setter
    def initial(self, initial):
        self._initial = initial

    @property
    def integral(self):
        return self._integral

    @integral.setter
    def integral(self, integral):
        self._integral = integral

    @property
    def time_points(self):
        """Read-only accessor for the list of time points of this time step
        """
        return np.array([step.time_point for step in self], dtype=float)

    @property
    def values(self):
        return np.append([self.initial.value.copy()], [step.value.copy() for step in self], axis=0)

    @property
    def rhs(self):
        if self.initial.rhs_evaluated and np.all([step.rhs_evaluated for step in self]):
            return np.append([self.initial.rhs], [step.rhs for step in self], axis=0)
        else:
            return None

    @values.setter
    def values(self, values):
        assert_condition(values.shape[0] == (len(self) + 1), ValueError,
                         "Number of values does not match number of nodes: %d != %d"
                         % (values.shape[0], (len(self) + 1)),
                         checking_obj=self)
        for _step in range(0, len(self)):
            self[_step].value = values[_step + 1].copy()

    @property
    def fas_correction(self):
        _fas = np.empty(len(self) + 1, dtype=np.object)
        _fas_shape = ()
        for step_i in range(0, len(self)):
            if self[step_i].has_fas_correction():
                _fas_shape = self[step_i].fas_correction.shape
                _fas[step_i + 1] = self[step_i].fas_correction.copy()

        if len(_fas_shape) > 0:
            _fas[0] = np.zeros(_fas_shape)
            return _fas
        else:
            return None

    @fas_correction.setter
    def fas_correction(self, fas_correction):
        assert_condition(fas_correction.shape[0] == (len(self) + 1), ValueError,
                         "Number of FAS Corrections does not match number of nodes: %d != %d"
                         % (fas_correction.shape[0], (len(self) + 1)),
                         checking_obj=self)
        for _step in range(0, len(self)):
            self[_step].fas_correction = fas_correction[_step + 1] - fas_correction[_step]

    @property
    def coarse_corrections(self):
        return np.append([np.zeros(self[0].coarse_correction.shape)], [step.coarse_correction for step in self], axis=0)

    @coarse_corrections.setter
    def coarse_corrections(self, coarse_correction):
        assert_condition(coarse_correction.shape[0] == (len(self) + 1), ValueError,
                         "Number of Coarse Corrections does not match number of nodes: %d != %d"
                         % (coarse_correction.shape[0], (len(self) + 1)),
                         checking_obj=self)
        for _step in range(0, len(self)):
            self[_step].coarse_correction = coarse_correction[_step + 1]


class MlSdcSolverState(SolverState):
    def __init__(self, **kwargs):
        kwargs['element_type'] = [MlSdcLevelState, TimeStepState, MlSdcNodeState]
        kwargs['solution_type'] = [FinalSolution, IterativeSolution, TrajectorySolutionData]
        super(MlSdcSolverState, self).__init__(**kwargs)

        assert_named_argument('num_nodes', kwargs, types=int, descriptor='Number of Nodes per Time Step')
        assert_named_argument('num_level', kwargs, types=int, descriptor='Number of Levels')
        kwargs['num_states'] = [kwargs.get['num_level'], kwargs.get('num_time_steps', 1), kwargs['num_nodes']]
        if 'num_time_steps' in kwargs:
            del kwargs['num_time_steps']
        del kwargs['num_nodes']
        del kwargs['num_level']
        super(SolverState, self).__init__(**kwargs)

    @property
    def num_level(self):
        """Read-only accessor for the number of levels

        Returns
        -------
        num_level : :py:class:`int`
        """
        return len(self)


__all__ = ['MlSdcStepState', 'MlSdcLevelState', 'MlSdcSolverState']
