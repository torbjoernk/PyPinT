# coding=utf-8
import unittest

from pypint.utilities.states.state_sequence import StateSequence
from pypint.utilities.states.node_state import NodeState
from pypint.utilities.data_structures.scalar_1d import Scalar1D
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData


class StateSequenceTest(unittest.TestCase):
    def setUp(self):
        self.default = StateSequence(solution_type=TrajectorySolutionData,
                                     element_type=NodeState,
                                     num_states=3,
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

    def test_initialization(self):
        _test_obj = StateSequence(solution_type=TrajectorySolutionData,
                                  element_type=NodeState,
                                  num_states=3,
                                  type=Scalar1D)
        self.assertEqual(len(_test_obj), 3)
        self.assertFalse(_test_obj.finalized)
        self.assertEqual(_test_obj.current_index, 0)

        with self.assertRaises(ValueError):
            StateSequence(element_type=NodeState,
                          num_states=3,
                          type=Scalar1D)
        with self.assertRaises(ValueError):
            StateSequence(solution_type=TrajectorySolutionData,
                          num_states=3,
                          type=Scalar1D)
        with self.assertRaises(ValueError):
            StateSequence(solution_type=TrajectorySolutionData,
                          element_type=NodeState,
                          type=Scalar1D)
        with self.assertRaises(ValueError):
            StateSequence(solution_type=TrajectorySolutionData,
                          element_type=NodeState,
                          num_states=3)

    def test_values_can_be_broadcasted(self):
        for step in self.default:
            self.assertEqual(step.value.value, 0.0)

        self.default.broadcast(Scalar1D(42.0))

    def test_provides_element_access_and_proceeding(self):
        _first = self.default._states[0]
        _second = self.default._states[1]
        _third = self.default._states[2]

        self.assertEqual(self.default.first_index, 0)
        self.assertEqual(self.default.first, _first)
        self.assertEqual(self.default.last_index, 2)
        self.assertEqual(self.default.last, _third)

        self.assertEqual(self.default.current_index, 0)
        self.assertEqual(self.default.current, _first)
        self.assertEqual(self.default.next_index, 1)
        self.assertEqual(self.default.next, _second)
        self.assertIsNone(self.default.previous_index)
        self.assertIsNone(self.default.previous)
        self.default.proceed()
        self.assertEqual(self.default.current_index, 1)
        self.assertEqual(self.default.current, _second)
        self.assertEqual(self.default.next_index, 2)
        self.assertEqual(self.default.next, _third)
        self.assertEqual(self.default.previous_index, 0)
        self.assertEqual(self.default.previous, _first)
        self.default.proceed()
        self.assertEqual(self.default.current_index, 2)
        self.assertEqual(self.default.current, _third)
        self.assertIsNone(self.default.next_index)
        self.assertIsNone(self.default.next)
        self.assertEqual(self.default.previous_index, 1)
        self.assertEqual(self.default.previous, _second)
        with self.assertRaises(StopIteration):
            self.default.proceed()
        self.assertEqual(self.default.current_index, 2)

        self.default._finalized = True
        with self.assertRaises(RuntimeError):
            self.default.proceed()

    def test_can_be_resetted(self):
        self.default.proceed()
        self.assertEqual(self.default.current_index, 1)
        self.default.reset_current_index()
        self.assertEqual(self.default.current_index, 0)

    def test_can_be_finalized(self):
        self.assertFalse(self.default.finalized)

        with self.assertRaises(RuntimeError):
            self.default._finalized = True
            self.default.finalized
        self.default._finalized = False

        self.default[0].value = self._first.value
        self.default[0].solution.time_point = self._first.time_point
        self.default[1].value = self._second.value
        self.default[1].solution.time_point = self._second.time_point
        self.default[2].value = self._third.value
        self.default[2].solution.time_point = self._third.time_point

        self.default.finalize()
        self.assertTrue(self.default.finalized)
        self.assertEqual(self.default.solution[0].value.value, self._first.value.value)
        self.assertEqual(self.default.solution[0].time_point, self._first.time_point)
        self.assertEqual(self.default.solution[1].value.value, self._second.value.value)
        self.assertEqual(self.default.solution[1].time_point, self._second.time_point)

    def test_can_be_nested_in_hierarchy(self):
        _parent = StateSequence(solution_type=[TrajectorySolutionData, TrajectorySolutionData],
                                element_type=[StateSequence, NodeState],
                                num_states=[3, 2],
                                type=Scalar1D)
        for _child in _parent:
            self.assertEqual(_child.parent, _parent)
        self.assertEqual(_parent[0].next_sibling, _parent[1])
        self.assertIsNone(_parent[0].previous_sibling)
        self.assertEqual(_parent[1].previous_sibling, _parent[0])
        self.assertEqual(_parent[1].next_sibling, _parent[2])
        self.assertEqual(_parent[2].previous_sibling, _parent[1])
        self.assertIsNone(_parent[2].next_sibling)

        self.assertIsNone(_parent.previous_sibling)
        self.assertIsNone(_parent.next_sibling)

    def test_provides_stringification(self):
        self.assertRegex(str(self.default), '^StateSequence<0x[0-9a-f]*>\(size=3\)')
        self.assertRegex(repr(self.default), '^<StateSequence at 0x[0-9a-f]* : size=3>')


if __name__ == '__main__':
    unittest.main()
