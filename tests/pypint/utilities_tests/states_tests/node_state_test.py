# coding=utf-8
import unittest

from pypint.utilities.states.node_state import NodeState
from pypint.utilities.data_structures.scalar_1d import Scalar1D


class NodeStateTest(unittest.TestCase):
    def setUp(self):
        self._default = NodeState(type=Scalar1D)

    def test_has_parent_accessor(self):
        self.assertIsNone(self._default.parent)

    def test_has_value_accessor(self):
        self.assertIsInstance(self._default.value, Scalar1D)

        with self.assertRaises(ValueError):
            self._default.value = 3

        self._default.value = Scalar1D(3.0)
        self.assertEqual(self._default.value.value, 3.0)

    def test_has_time_point_accessor(self):
        self.assertIsNone(self._default.time_point)

        with self.assertRaises(AttributeError):
            self._default.time_point = 0.0

        self._default.solution.time_point = 0.0
        self.assertEqual(self._default.time_point, 0.0)

    def test_has_delta_tau_accessor(self):
        self.assertEqual(self._default.delta_tau, 0.0)

        with self.assertRaises(ValueError):
            self._default.delta_tau = 'not a float'

        with self.assertRaises(ValueError):
            self._default.delta_tau = -0.5

        self._default.delta_tau = 1.0
        self.assertEqual(self._default.delta_tau, 1.0)
        self._default.delta_tau = 0.0
        self.assertEqual(self._default.delta_tau, 0.0)

    def test_its_solution_can_be_finalized(self):
        self.assertFalse(self._default.solution.finalized)

        self._default.value = Scalar1D(3.0)
        self.assertEqual(self._default.value.value, 3.0)

        self._default.finalize()
        self.assertTrue(self._default.solution.finalized)
        self.assertEqual(self._default.value.value, 3.0)
        self.assertIsInstance(self._default.solution.value, Scalar1D)
        self.assertEqual(self._default.solution.value.value, 3.0)

    def test_can_store_rhs_evaluation(self):
        self.assertIsInstance(self._default.rhs, Scalar1D)

        self._default.rhs = Scalar1D(42)
        self.assertEqual(self._default.rhs.value, 42)

        with self.assertRaises(ValueError):
            self._default.rhs = 42

    def test_can_store_integral_evaluation(self):
        self.assertIsInstance(self._default.integral, Scalar1D)

        self._default.integral = Scalar1D(42)
        self.assertEqual(self._default.integral.value, 42)

        with self.assertRaises(ValueError):
            self._default.integral = 42

    def test_provides_stringification(self):
        self.assertRegex(str(self._default), '^NodeState<0x[0-9a-f]*>\(data=Scalar1D<.*\)\)')
        self.assertRegex(repr(self._default), '^<NodeState at 0x[0-9a-f]* : data=<Scalar1D at .*>>')

        self.assertIsNotNone(self._default.lines_for_log())
        self.assertIn('Value', self._default.lines_for_log())
        self.assertIn('Solution', self._default.lines_for_log())
        self.assertIn('Delta Tau', self._default.lines_for_log())
        self.assertIn('RHS', self._default.lines_for_log())
        self.assertIn('Integral', self._default.lines_for_log())


if __name__ == '__main__':
    unittest.main()
