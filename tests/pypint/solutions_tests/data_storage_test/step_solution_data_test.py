# coding=utf-8
import numpy

from pypint.solutions.data_storage.step_solution_data import StepSolutionData
from pypint.utilities.data_structures.scalar_1d import Scalar1D
from pypint.solvers.diagnosis import Error, Residual
from tests import NumpyAwareTestCase


class StepSolutionDataTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = StepSolutionData()

        self._value = Scalar1D(value=1.0, dtype=numpy.float)
        self._error = Error(value=numpy.array([1.0], dtype=numpy.float))
        self._residual = Residual(value=numpy.array([0.01], dtype=numpy.float))

    def test_provides_value(self):
        self.assertIsNone(self._default.value, "Default value is 'None'.")

        self._default.value = self._value
        self.assertEqual(self._default.value, self._value)
        self.assertEqual(self._default.dim, self._value.dim)
        self.assertEqual(self._default.dtype, self._value.dtype)

        self._default.finalize()
        with self.assertRaises(AttributeError):
            self._default.value = self._value

        _test = StepSolutionData(value=self._value)
        self.assertEqual(_test.dim, self._value.dim)
        self.assertEqual(_test.dtype, self._value.dtype)
        self.assertEqual(_test.value, self._value)

        with self.assertRaises(ValueError):
            StepSolutionData(value="not numpy.ndarray")

    def test_provides_time_point(self):
        self.assertIsNone(self._default.time_point)

        self._default.time_point = 1.0
        self.assertEqual(self._default.time_point, 1.0)

        self._default.finalize()
        with self.assertRaises(AttributeError):
            self._default.time_point = 0.0

        _test = StepSolutionData(time_point=0.0)
        self.assertEqual(_test.time_point, 0.0)

        with self.assertRaises(ValueError):
            StepSolutionData(time_point="not float")

    def test_provides_error(self):
        self.assertIsNone(self._default.error)

        self._default.error = self._error
        self.assertEqual(self._default.error, self._error)

        self._default.finalize()
        with self.assertRaises(AttributeError):
            self._default.error = self._error

        _test = StepSolutionData(error=self._error)
        self.assertEqual(_test.error, self._error)

        with self.assertRaises(ValueError):
            StepSolutionData(error="not numpy.ndarray")

    def test_provides_residual(self):
        self.assertIsNone(self._default.residual)

        self._default.residual = self._residual
        self.assertEqual(self._default.residual, self._residual)

        self._default.finalize()
        with self.assertRaises(AttributeError):
            self._default.residual = self._residual

        _test = StepSolutionData(residual=self._residual)
        self.assertEqual(_test.residual, self._residual)

        with self.assertRaises(ValueError):
            StepSolutionData(residual="not numpy.ndarray")

    def test_is_comparable(self):
        _test1 = StepSolutionData(value=self._value, time_point=0.0, error=self._error, residual=self._residual)
        _test2 = StepSolutionData(value=self._value, time_point=0.0, error=self._error, residual=self._residual)
        self.assertTrue(_test1 == _test2)
        self.assertTrue(_test1.__eq__(_test2))
        self.assertFalse(_test1 != _test2)
        self.assertFalse(_test1.__ne__(_test2))

        _test2.time_point = 1.0
        self.assertTrue(_test1 < _test2)
        self.assertTrue(_test1.__lt__(_test2))
        self.assertTrue(_test1 <= _test2)
        self.assertTrue(_test1.__le__(_test2))
        self.assertFalse(_test1 > _test2)
        self.assertFalse(_test1.__gt__(_test2))
        self.assertFalse(_test1 >= _test2)
        self.assertFalse(_test1.__ge__(_test2))

    def test_provides_stringification(self):
        _test1 = StepSolutionData(value=self._value, time_point=0.0, error=self._error, residual=self._residual)

        self.assertRegex(str(_test1), '^StepSolutionData<0x[0-9a-f]*>\(value=.*Scalar1D.*, time_point=0.0, finalized=False\)')
        self.assertRegex(repr(_test1), '^<StepSolutionData at 0x[0-9a-f]* : value=.*Scalar1D.*, time_point=0.0, finalized=False>')

        self.assertIsNotNone(_test1.lines_for_log())
        self.assertIn('Finalized', _test1.lines_for_log())
        self.assertIn('Time Point', _test1.lines_for_log())
        self.assertIn('Value', _test1.lines_for_log())
        self.assertIn('Error', _test1.lines_for_log())
        self.assertIn('Residual', _test1.lines_for_log())

if __name__ == '__main__':
    import unittest
    unittest.main()
