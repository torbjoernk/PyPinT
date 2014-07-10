# coding=utf-8
import unittest

from pypint.utilities.states.solver_state import SolverState
from pypint.utilities.states.iteration_state import IterationState
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.solutions.final_solution import FinalSolution
from pypint.solutions.iterative_solution import IterativeSolution
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.utilities.states.state_sequence import StateSequence
from pypint.utilities.states.node_state import NodeState
from pypint.utilities.data_structures.scalar_1d import Scalar1D


class SolverStateTest(unittest.TestCase):
    def setUp(self):
        _ = SolverState(element_type=[IterationState, StateSequence, NodeState],
                        num_states=[3, 0, 2],
                        type=Scalar1D)
        self.default = SolverState(solution_type=[FinalSolution, IterativeSolution, TrajectorySolutionData],
                                   element_type=[IterationState, StateSequence, NodeState],
                                   num_states=[3, 0, 2],
                                   type=Scalar1D)

    def test_provides_interval_width(self):
        self.assertEqual(self.default.delta_interval, 0.0)

        self.default.delta_interval = 1.0
        self.assertEqual(self.default.delta_interval, 1.0)

    def test_has_special_proxy_accessors(self):
        self.assertEqual(self.default.current_iteration, self.default.current)
        self.assertEqual(self.default.current_iteration_index, self.default.current_index)
        self.assertIsNone(self.default.previous_iteration)
        self.assertTrue(self.default.is_first_iteration)

        self.default.proceed()
        self.assertEqual(self.default.current_iteration, self.default.current)
        self.assertEqual(self.default.current_iteration_index, self.default.current_index)
        self.assertEqual(self.default.previous_iteration, self.default.previous)
        self.assertEqual(self.default.previous_iteration_index, self.default.previous_index)

        self.assertEqual(self.default.first_iteration, self.default.first)
        self.assertFalse(self.default.is_first_iteration)

        self.default.reset_current_index()
        self.assertEqual(self.default.last_iteration, self.default.last)
        self.assertEqual(self.default.last_iteration_index, self.default.last_index)


if __name__ == '__main__':
    unittest.main()
