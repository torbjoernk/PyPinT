# coding=utf-8
import unittest

from pypint.utilities.states.level_state import LevelState
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.solutions.iterative_solution import IterativeSolution
from pypint.utilities.states.state_sequence import StateSequence
from pypint.utilities.states.node_state import NodeState
from pypint.utilities.data_structures.scalar_1d import Scalar1D


class LevelStateTest(unittest.TestCase):
    def setUp(self):
        _ = LevelState(solution_type=[IterativeSolution, TrajectorySolutionData],
                                  # element_type=[StateSequence, NodeState],
                                  num_states=[0, 3],
                                  type=Scalar1D)
        self.default = LevelState(solution_type=[IterativeSolution, TrajectorySolutionData],
                                  element_type=[StateSequence, NodeState],
                                  num_states=[0, 3],
                                  type=Scalar1D)

    def test_provides_intermediate_states(self):
        self.assertIsNone(self.default.intermediate)

        self.default.reset_intermediate()
        self.assertIsInstance(self.default.intermediate, StateSequence)

        _test = StateSequence(solution_type=TrajectorySolutionData,
                              element_type=NodeState,
                              num_states=3,
                              type=Scalar1D)
        self.default.intermediate = _test
        self.assertEqual(self.default.intermediate, _test)


if __name__ == '__main__':
    unittest.main()
