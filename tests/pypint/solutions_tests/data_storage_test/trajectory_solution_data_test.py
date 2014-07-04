# coding=utf-8
import warnings
from copy import deepcopy

import numpy

from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.solutions.data_storage.step_solution_data import StepSolutionData
from pypint.solvers.diagnosis import Error, Residual
from pypint.utilities.data_structures.scalar_1d import Scalar1D
from tests import NumpyAwareTestCase


class TrajectorySolutionDataTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = TrajectorySolutionData()

        self._element1 = StepSolutionData(value=Scalar1D(value=1.0), time_point=0.0,
                                          error=Error(numpy.array([1.0])), residual=Residual(numpy.array([0.5])))
        self._element2 = StepSolutionData(value=Scalar1D(value=1.0), time_point=0.5,
                                          error=Error(numpy.array([1.0])), residual=Residual(numpy.array([0.5])))

    def test_solutions_can_be_added(self):
        self._default.add_solution_data(value=Scalar1D(value=1.0), time_point=0.1)
        self.assertEqual(len(self._default.data), 1)
        self.assertEqual(len(self._default), 1)
        self.assertNumpyArrayEqual(self._default.time_points, numpy.array([0.1]))
        self.assertEqual(self._default.values[0], Scalar1D(value=1.0))

        warnings.simplefilter("ignore")  # each of the following tests emits a warning about failed consistency
        self.assertRaises(ValueError,
                          self._default.add_solution_data, value="not numpy.ndarray", time_point=1.0)
        self.assertRaises(ValueError,
                          self._default.add_solution_data, value=numpy.array(["not", "object"]), time_point=1.0)
        self.assertRaises(ValueError,
                          self._default.add_solution_data,
                          value=numpy.array(["is", "StepSolutionData", False], dtype=object), time_point=1.0)
        self.assertRaises(ValueError,
                          self._default.add_solution_data, value=numpy.array([1.0, 2.0, 3.0]), time_point=1.0)
        warnings.resetwarnings()

    def test_solutions_can_be_deleted(self):
        self._default.append(self._element1)
        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)

        del self._default[0]
        self.assertEqual(len(self._default), 1)
        self.assertEqual(self._default[0], self._element2)

        with self.assertRaises(IndexError):
            del self._default[1]

    def test_solutions_can_be_replaced(self):
        self._default.append(self._element1)
        self.assertEqual(len(self._default), 1)

        _element1b = deepcopy(self._element1)
        _element1b.value = Scalar1D(0.0)
        self._default.set_at(0.0, _element1b)
        self.assertEqual(self._default[0], _element1b)
        self.assertNotEqual(self._default[0], self._element1)

        self._default[0] = self._element1
        self.assertEqual(self._default[0], self._element1)
        self.assertNotEqual(self._default[0], _element1b)

        with self.assertRaises(ValueError):
            self._default.set_at(0.5, self._element2)

        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)
        with self.assertRaises(ValueError):
            _test = StepSolutionData(value=Scalar1D(42.0), time_point=1.0)
            self._default.set_at(0.0, _test)

    def test_can_be_finalized(self):
        self._default.append(self._element1)
        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)

        self.assertFalse(self._default.finalized)
        self._default.finalize()
        self.assertTrue(self._default.finalized)

    def test_provides_indexing(self):
        self._default.append(self._element1)
        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)

        self.assertEqual(self._default[0], self._element1)
        self.assertEqual(self._default.at(0.0), self._element1)
        self.assertIsNone(self._default.at(1.0))

        with self.assertRaises(IndexError):
            self._default[2]

    def test_provides_raw_data(self):
        self.assertListEqual(self._default.data, [])

        self._default.append(self._element1)
        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)

        self.assertListEqual(self._default.data, [self._element1, self._element2])

        with self.assertRaises(AttributeError):
            self._default.data = "read-only"

    def test_provides_values(self):
        self.assertNumpyArrayEqual(self._default.values, numpy.zeros(0, dtype=numpy.object))

        self._default.append(self._element1)
        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)

        self.assertNumpyArrayEqual(self._default.values, numpy.asarray([Scalar1D(1.0), Scalar1D(1.0)]))

        with self.assertRaises(AttributeError):
            self._default.values = "read-only"

    def test_provides_time_points(self):
        self.assertNumpyArrayEqual(self._default.time_points, numpy.zeros(0, dtype=numpy.float))

        self._default.append(self._element1)
        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)

        self.assertNumpyArrayEqual(self._default.time_points, numpy.asarray([0.0, 0.5]))

        with self.assertRaises(AttributeError):
            self._default.time_points = "read-only"

    def test_provides_errors(self):
        self.assertNumpyArrayEqual(self._default.errors, numpy.zeros(0, dtype=numpy.object))

        with self.assertRaises(AttributeError):
            self._default.errors = "read-only"

    def test_provides_residuals(self):
        self.assertNumpyArrayEqual(self._default.residuals, numpy.zeros(0, dtype=numpy.object))

        with self.assertRaises(AttributeError):
            self._default.residuals = "read-only"

    def test_is_iterable(self):
        self._default.append(self._element1)
        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)

        for elem in self._default:
            self.assertIsInstance(elem, StepSolutionData)

    def test_provides_stringification(self):
        self._default.append(self._element1)
        self._default.append(self._element2)
        self.assertEqual(len(self._default), 2)

        self.assertRegex(str(self._default), '^TrajectorySolutionData<0x[0-9a-f]*>\(data=.*, time_points=.*\)$')
        self.assertRegex(repr(self._default), '^<TrajectorySolutionData at 0x[0-9a-f]* : data=.*, time_points=.*>$')

        self.assertIsNotNone(self._default.lines_for_log())
        self.assertIn('Data', self._default.lines_for_log())
        self.assertIn('Time Points', self._default.lines_for_log())


if __name__ == '__main__':
    import unittest
    unittest.main()
