# coding=utf-8
from unittest.mock import MagicMock
from nose.tools import *
import numpy

from pypint.utilities.quadrature.weights.polynomial_weights import PolynomialWeights
from pypint.utilities.quadrature.weights.abstract_weights import AbstractWeights
from pypint.utilities.quadrature.nodes.gauss_lobatto_nodes import GaussLobattoNodes
from tests import NumpyAwareTestCase, assert_numpy_array_almost_equal, assert_numpy_array_equal


test_coefficients = [
    numpy.asarray([42, 0.0, 3.14])
]

# Tests for w(x) = 1 as weighting function
TEST_DATA = \
    [
        {
            'nodes': MagicMock(GaussLobattoNodes, '2 Gauss-Lobatto Nodes',
                               nodes=numpy.array([-1.0, 1.0]),
                               num_nodes=2,
                               interval=numpy.array([-1.0, 1.0])),
            'expected': numpy.asarray([1.0, 1.0])
        },
        {
            'nodes': MagicMock(GaussLobattoNodes, '3 Gauss-Lobatto Nodes',
                               nodes=numpy.array([-1.0, 0.0, 1.0]),
                               num_nodes=3,
                               interval=numpy.array([-1.0, 1.0])),
            'expected': numpy.asarray([1.0 / 3.0, 4.0 / 3.0, 1.0 / 3.0])
        },
        {
            'nodes': MagicMock(GaussLobattoNodes, '5 Gauss-Lobatto Nodes',
                               nodes=numpy.array([-1.0, -numpy.sqrt(3.0 / 7.0), 0.0, numpy.sqrt(3.0 / 7.0), 1.0]),
                               num_nodes=5,
                               interval=numpy.array([-1.0, 1.0])),
            'expected': numpy.asarray([1.0 / 10.0, 49.0 / 90.0, 32.0 / 45.0, 49.0 / 90.0, 1.0 / 10.0])
        }
    ]


def constant_weight_function(nodes, expected_weights):
    _weight_function = PolynomialWeights(1.0)
    _weight_function.compute_weights(nodes)
    assert_numpy_array_almost_equal(_weight_function.weights, expected_weights)


def test_standard_gauss_lobatto_weights():
    for data_set in TEST_DATA:
        yield constant_weight_function, data_set['nodes'], data_set['expected']


class PolynomialWeightFunctionTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = PolynomialWeights()

    def test_is_abstract_weight_function(self):
        self.assertIsInstance(self._default, AbstractWeights)

    def test_provides_coefficient_accessor(self):
        self.assertNumpyArrayEqual(self._default.coefficients, numpy.asarray([1.0]))
        self._default.add_coefficient(1.2, 2)
        self.assertNumpyArrayEqual(self._default.coefficients, numpy.asarray([1.0, 0.0, 1.2]))

        _test = PolynomialWeights(1.1, 1.2)
        self.assertNumpyArrayEqual(_test.coefficients, numpy.asarray([1.1, 1.2]))
        del _test
        _test = PolynomialWeights([1.2, 1.3])
        self.assertNumpyArrayEqual(_test.coefficients, numpy.asarray([1.2, 1.3]))

    def test_provides_weights_accessor(self):
        self.assertIsNone(self._default.weights)

    def test_provides_stringification(self):
        self.assertRegex(str(self._default),
                         '^PolynomialWeights<0x[0-9a-f]*>\(weights=None, coeffs=\[ 1\.\]\)')

        self.assertRegex(repr(self._default),
                         '^<PolynomialWeights at 0x[0-9a-f]* : weights=None, coeffs=\[ 1\.\]>')

        self.assertIsNotNone(self._default.lines_for_log())
        self.assertIn('Type', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Type'], 'Polynomial')
        self.assertIn('Weights', self._default.lines_for_log())
        self.assertIn('Coefficients', self._default.lines_for_log())
        self.assertRegex(self._default.lines_for_log()['Coefficients'], '\[ 1\.\]')


if __name__ == "__main__":
    import unittest
    unittest.main()
