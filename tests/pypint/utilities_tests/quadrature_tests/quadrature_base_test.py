# coding=utf-8
"""
.. moduleauthor: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from unittest.mock import MagicMock
import numpy

from pypint.utilities.quadrature.quadrature_base import QuadratureBase
from pypint.utilities.quadrature.nodes.abstract_nodes import AbstractNodes
from pypint.utilities.quadrature.weights.abstract_weights import AbstractWeights
from pypint.utilities.data_structures.abstract_spatial_object import AbstractSpatialObject
from pypint.utilities.quadrature import QUADRATURE_PRESETS
from tests import NumpyAwareTestCase


class IntegratorBaseTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = QuadratureBase()

        self._spatial_obj = MagicMock(AbstractSpatialObject, 'a Spatial Object')

    def test_has_accessors_for_nodes(self):
        self.assertIsNone(self._default.nodes)
        self.assertIsNone(self._default.nodes_type)

        self._default.init(**QUADRATURE_PRESETS['Gauss-Lobatto'])
        self.assertIsInstance(self._default.nodes_type, AbstractNodes)
        self.assertIsInstance(self._default.nodes, numpy.ndarray)

    def test_has_accessors_for_weights(self):
        self.assertIsNone(self._default.weights)
        self.assertIsNone(self._default.weights_function)

        self._default.init(**QUADRATURE_PRESETS['Gauss-Lobatto'])
        self.assertIsInstance(self._default.weights_function, AbstractWeights)
        self.assertIsInstance(self._default.weights, numpy.ndarray)

    def test_interval_transformation(self):
        self._default.init(**QUADRATURE_PRESETS['Gauss-Lobatto'])
        self._default.transform_interval(numpy.asarray([0.0, 1.0]))
        self.assertNumpyArrayEqual(self._default.nodes_type.interval, numpy.asarray([0.0, 1.0]))

    def test_can_be_applied(self):
        self.assertIsNone(self._default.num_nodes)
        self._default.init(**QUADRATURE_PRESETS['Gauss-Lobatto'])
        self._default.apply([self._spatial_obj, self._spatial_obj, self._spatial_obj])

        with self.assertRaises(ValueError):
            self._default.apply([])

        with self.assertRaises(ValueError):
            self._default.apply([self._spatial_obj])

        with self.assertRaises(ValueError):
            self._default.apply([self._spatial_obj, self._spatial_obj, 'not a SpatialObject'])

    def test_provides_stringification(self):
        self.assertRegex(str(self._default), '^QuadratureBase<0x[0-9a-f]*>\(nodes=None, weights=None\)$')
        self.assertRegex(repr(self._default), '^<QuadratureBase at 0x[0-9a-f]* : nodes=None, weights=None>$')
        self.assertIsNotNone(self._default.lines_for_log())
        self.assertIn('Nodes', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Nodes'], 'na')
        self.assertIn('Weights Function', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Weights Function'], 'na')


if __name__ == "__main__":
    import unittest
    unittest.main()
