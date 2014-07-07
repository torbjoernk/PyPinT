# coding=utf-8
import unittest

from pypint.utilities.states.mutable_state_sequence import MutableStateSequence
from pypint.utilities.states.node_state import NodeState
from pypint.utilities.data_structures.scalar_1d import Scalar1D
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData


class MutableStateSequenceTest(unittest.TestCase):
    def setUp(self):
        _ = MutableStateSequence(solution_type=TrajectorySolutionData,
                                 element_type=NodeState,
                                 type=Scalar1D)
        self.default = MutableStateSequence(solution_type=TrajectorySolutionData,
                                            element_type=NodeState,
                                            num_states=0,
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

    def test_elements_can_be_appended_and_inserted(self):
        self.assertEqual(len(self.default), 0)

        self.default.append(self._first)
        self.assertEqual(len(self.default), 1)
        self.assertEqual(self.default[0].value, self._first.value)

        self.default.insert(0, self._second)
        self.assertEqual(len(self.default), 2)
        self.assertEqual(self.default[1].value, self._first.value)
        self.assertEqual(self.default[0].value, self._second.value)

    def test_elements_can_be_deleted(self):
        self.assertEqual(len(self.default), 0)

        self.default.append(self._first)
        self.default.append(self._second)
        self.assertEqual(len(self.default), 2)
        self.assertEqual(self.default[0].value, self._first.value)
        self.assertEqual(self.default[1].value, self._second.value)

        del self.default[0]
        self.assertEqual(len(self.default), 1)
        self.assertEqual(self.default[0].value, self._second.value)

        with self.assertRaises(IndexError):
            del self.default[1]

    def test_elements_can_be_replaced(self):
        self.assertEqual(len(self.default), 0)

        self.default.append(self._first)
        self.default.append(self._second)
        self.assertEqual(len(self.default), 2)
        self.assertEqual(self.default[0].value, self._first.value)
        self.assertEqual(self.default[1].value, self._second.value)

        self.default[0] = self._third
        self.assertEqual(len(self.default), 2)
        self.assertEqual(self.default[0].value, self._third.value)


if __name__ == '__main__':
    unittest.main()
