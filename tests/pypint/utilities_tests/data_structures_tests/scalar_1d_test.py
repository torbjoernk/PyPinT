# coding=utf-8
import unittest
from copy import copy, deepcopy

import numpy as np

from pypint.utilities.data_structures.scalar_1d import Scalar1D
from pypint.utilities.data_structures.abstract_spatial_object import AbstractSpatialObject
from pypint.utilities.abc import Copyable, Deepcopyable


class Scalar1DTest(unittest.TestCase):
    def setUp(self):
        self._default = Scalar1D()

    def test_is_abstract_spatial_object(self):
        # this does imply, that Scalar1D has the same behaviour as an AbstractSpatialObject;
        #  but is a strong indicator that it does so
        self.assertIsInstance(self._default, AbstractSpatialObject)

    def test_constructor_takes_value(self):
        _positional = Scalar1D(1.0)
        self.assertEqual(_positional.value, 1.0)

        _keyword = Scalar1D(value=1.0)
        self.assertEqual(_keyword.value, 1.0)

    def test_constructor_takes_numeric_type(self):
        _test = Scalar1D(dtype=np.complex128)
        self.assertIs(_test.dtype, np.dtype('complex128'))

    def test_has_dtype(self):
        self.assertIs(self._default.dtype, np.dtype('float64'))

        self._default.dtype = np.dtype(np.complex)
        self.assertIs(self._default.dtype, np.dtype('complex'))

        self._default.dtype = np.float16
        self.assertIs(self._default.dtype, np.dtype('float16'))

        with self.assertRaises(ValueError):
            self._default.dtype = np.dtype('str')

        with self.assertRaises(ValueError):
            self._default.dtype = np.dtype('object')

    def test_has_value_accessor(self):
        self.assertEqual(self._default.value, 0.0)

    def test_has_value_setter(self):
        self._default.set(1.0)
        self.assertEqual(self._default.value, 1.0)

        with self.assertRaises(ValueError):
            self._default.set('a string')

        with self.assertRaises(ValueError):
            self._default.set([1.0])

    def test_cannot_change_dimension(self):
        with self.assertRaises(RuntimeError):
            self._default.dim = 2

    def test_has_norm(self):
        self.assertEqual(self._default.norm, 0.0)

    def test_has_addition_operator(self):
        _result = self._default + 1.0
        self.assertEqual(_result.value, 1.0)

        _result = self._default + Scalar1D(value=1.0, dtype=np.dtype(np.float))
        self.assertEqual(_result.value, 1.0)

        with self.assertRaises(TypeError):
            self._default + 'str'

        with self.assertRaises(TypeError):
            self._default + [1.0]

        with self.assertRaises(TypeError):
            self._default += 'str'

        with self.assertRaises(TypeError):
            self._default += [1.0]

        self._default += 1.0
        self.assertEqual(self._default.value, 1.0)

    def test_has_subtraction_operator(self):
        _result = self._default - 1.0
        self.assertEqual(_result.value, -1.0)

        _result = self._default - Scalar1D(value=1.0, dtype=np.dtype(np.float))
        self.assertEqual(_result.value, -1.0)

        with self.assertRaises(TypeError):
            self._default - 'str'

        with self.assertRaises(TypeError):
            self._default - [1.0]

        with self.assertRaises(TypeError):
            self._default -= 'str'

        with self.assertRaises(TypeError):
            self._default -= [1.0]

        self._default -= 1.0
        self.assertEqual(self._default.value, -1.0)

    def test_has_multiplication_operator(self):
        _result = self._default * 1.0
        self.assertEqual(_result.value, 0.0)

        with self.assertRaises(TypeError):
            self._default * Scalar1D(value=1.0, dtype=np.dtype(np.float))

        with self.assertRaises(TypeError):
            self._default * 'str'

        with self.assertRaises(TypeError):
            self._default * [1.0]

        with self.assertRaises(TypeError):
            self._default *= 'str'

        with self.assertRaises(TypeError):
            self._default *= [1.0]

        self._default *= 1.0
        self.assertEqual(self._default.value, 0.0)

    def test_has_negative_and_positive_operator(self):
        self._default.set(1.0)
        self.assertEqual((-self._default).value, -1.0)
        self.assertEqual((+self._default).value, 1.0)

        self._default.set(-1.0)
        self.assertEqual((-self._default).value, 1.0)
        self.assertEqual((+self._default).value, -1.0)

    def test_is_copyable(self):
        self.assertIsInstance(self._default, Copyable)
        self._default.set(42)
        _copy = copy(self._default)
        self.assertEqual(_copy.value, self._default.value)
        self.assertEqual(_copy.dtype, self._default.dtype)
        self.assertNotEqual(id(_copy), id(self._default))
        self.assertEqual(id(_copy.dtype), id(self._default.dtype))
        self.assertEqual(id(_copy.value), id(self._default.value))

    def test_is_deepcopyable(self):
        self.assertIsInstance(self._default, Deepcopyable)
        self._default.set(42)
        _copy = deepcopy(self._default)
        self.assertEqual(_copy.value, self._default.value)
        self.assertEqual(_copy.dtype, self._default.dtype)
        self.assertNotEqual(id(_copy), id(self._default))
        self.assertNotEqual(id(_copy.dtype), id(self._default.dtype))
        self.assertNotEqual(id(_copy.value), id(self._default.value))

    def test_is_comparable(self):
        _one = Scalar1D(1.0)
        self.assertTrue(Scalar1D(1.0) == _one)
        self.assertFalse(Scalar1D(42) == _one)

        self.assertTrue(Scalar1D(0.0) <= _one)
        self.assertTrue(Scalar1D(0.0) < _one)
        self.assertTrue(Scalar1D(2.0) > _one)
        self.assertTrue(Scalar1D(2.0) >= _one)
        self.assertTrue(Scalar1D(2.0) != _one)

        self.assertEqual(_one.__eq__(42), NotImplemented)
        self.assertEqual(_one.__gt__(42), NotImplemented)

    def test_has_stringification(self):
        self.assertRegex(str(self._default), '^Scalar1D<0x[0-9a-f]*>\(dtype=.*, value=.*\)$')

        self.assertRegex(repr(self._default), '^<Scalar1D at 0x[0-9a-f]* : dtype=.*, value=.*\>$')

        self.assertIn('Numeric Type', self._default.lines_for_log())
        self.assertIn('Value', self._default.lines_for_log())


if __name__ == '__main__':
    unittest.main()
