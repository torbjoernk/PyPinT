# coding=utf-8
import numpy

from tests import NumpyAwareTestCase
from pypint.utilities.states.state_sequence import StateSequence
from pypint.utilities.states.timestep_state import TimeStepState
from pypint.utilities.states.node_state import NodeState
from pypint.utilities.data_structures.scalar_1d import Scalar1D
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData


class TimeStepStateTest(NumpyAwareTestCase):
    def setUp(self):
        self.default = TimeStepState(solution_type=TrajectorySolutionData,
                                     element_type=NodeState,
                                     num_states=3,
                                     type=Scalar1D)
        self._initial = NodeState(type=Scalar1D)
        self._initial.value = Scalar1D(41)
        self._initial.solution.time_point = 0.0
        self._first = NodeState(type=Scalar1D)
        self._first.value = Scalar1D(42)
        self._first.solution.time_point = 0.1
        self._second = NodeState(type=Scalar1D)
        self._second.value = Scalar1D(43)
        self._second.solution.time_point = 0.5
        self._third = NodeState(type=Scalar1D)
        self._third.value = Scalar1D(44)
        self._third.solution.time_point = 1.0

        self.default.initial_node = self._initial
        self.default._states[0] = self._first
        self.default._states[1] = self._second
        self.default._states[2] = self._third

        self.assertEqual(self.default[0], self._first)
        self.assertEqual(self.default[1], self._second)
        self.assertEqual(self.default[2], self._third)

    def test_is_a_state_sequence(self):
        self.assertIsInstance(self.default, StateSequence)

    def test_has_initial_node(self):
        self.assertIsInstance(self.default.initial_node, NodeState)
        self.assertEqual(self.default.initial_node, self._initial)

    def test_has_time_step_delta(self):
        self.assertEqual(self.default.delta_time_step, 0.0)

        self.default.delta_time_step = 0.5
        self.assertEqual(self.default.delta_time_step, 0.5)

        with self.assertRaises(ValueError):
            self.default.delta_time_step = -0.5

    def test_provides_list_of_all_time_points(self):
        self.assertNumpyArrayEqual(self.default.time_points, numpy.array([0.1, 0.5, 1.0]))

    def test_provides_time_points_accessors(self):
        self.assertEqual(self.default.previous_time_point, 0.0)
        self.assertEqual(self.default.current_time_point, 0.1)
        self.assertEqual(self.default.next_time_point, 0.5)

        self.default.proceed()
        self.assertEqual(self.default.previous_time_point, 0.1)
        self.assertEqual(self.default.current_time_point, 0.5)
        self.assertEqual(self.default.next_time_point, 1.0)

    def test_has_special_proxy_accessors(self):
        self.assertEqual(self.default.current_index, 0)
        self.assertEqual(self.default.current_node, self.default.current)
        self.assertEqual(self.default.current_node_index, self.default.current_index)
        self.assertEqual(self.default.previous_node, self.default.initial_node)
        self.assertIsNone(self.default.previous_node_index)
        self.assertEqual(self.default.next_node, self.default.next)
        self.assertEqual(self.default.next_node_index, self.default.next_index)

        self.default.proceed()
        self.assertEqual(self.default.current_index, 1)
        self.assertEqual(self.default.current_node, self.default.current)
        self.assertEqual(self.default.current_node_index, self.default.current_index)
        self.assertEqual(self.default.previous_node, self.default.previous)
        self.assertEqual(self.default.previous_node_index, self.default.previous_index)
        self.assertEqual(self.default.next_node, self.default.next)
        self.assertEqual(self.default.next_node_index, self.default.next_index)

        self.assertEqual(self.default.last_node, self.default.last)
        self.assertEqual(self.default.last_node_index, self.default.last_index)

    def test_provides_stringification(self):
        self.assertRegex(str(self.default), '^TimeStepState<0x[0-9a-f]*>\(size=3\)')
        self.assertRegex(repr(self.default), '^<TimeStepState at 0x[0-9a-f]* : size=3>')


if __name__ == '__main__':
    import unittest
    unittest.main()
