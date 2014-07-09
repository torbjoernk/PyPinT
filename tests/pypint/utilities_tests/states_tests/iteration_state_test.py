# coding=utf-8
import unittest

from pypint.utilities.states.iteration_state import IterationState
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.solutions.iterative_solution import IterativeSolution
from pypint.utilities.states.state_sequence import StateSequence
from pypint.utilities.states.node_state import NodeState
from pypint.utilities.data_structures.scalar_1d import Scalar1D


class IterationStateTest(unittest.TestCase):
    def setUp(self):
        self.default = IterationState(solution_type=[IterativeSolution, TrajectorySolutionData],
                                      element_type=[StateSequence, NodeState],
                                      num_states=[0, 3],
                                      type=Scalar1D)
        self._first = NodeState(type=Scalar1D)
        self._first.value = Scalar1D(42)
        self._first.solution.time_point = 0.0
        self._second = NodeState(type=Scalar1D)
        self._second.value = Scalar1D(43)
        self._second.solution.time_point = 0.5
        self._third = NodeState(type=Scalar1D)
        self._third.value = Scalar1D(44)
        self._third.solution.time_point = 1.0

    def test_can_proceed(self):
        self.assertEqual(len(self.default), 1)
        self.default.proceed()
        self.assertEqual(len(self.default), 2)

    def test_can_be_finalized(self):
        self.default[0][0].value = self._first.value
        self.default[0][0].solution.time_point = self._first.time_point
        self.default[0][1].value = self._second.value
        self.default[0][1].solution.time_point = self._second.time_point
        self.default[0][2].value = self._third.value
        self.default[0][2].solution.time_point = self._third.time_point

        self.assertFalse(self.default.finalized)
        for _state in self.default:
            self.assertFalse(_state.finalized)

        self.default.finalize()

        self.assertTrue(self.default.finalized)
        for _state in self.default:
            self.assertTrue(_state.finalized)

        self.assertEqual(self.default.solution[0][0].value.value, self._first.value.value)
        self.assertEqual(self.default.solution[0][0].time_point, self._first.time_point)
        self.assertEqual(self.default.solution[0][1].value.value, self._second.value.value)
        self.assertEqual(self.default.solution[0][1].time_point, self._second.time_point)


if __name__ == '__main__':
    unittest.main()
