# coding=utf-8
import numpy

from pypint.utilities.quadrature.sdc_quadrature import SdcQuadrature
from pypint.utilities.data_structures.scalar_1d import Scalar1D
from pypint.utilities.quadrature.nodes.gauss_lobatto_nodes import GaussLobattoNodes
from tests import NumpyAwareTestCase


class SdcIntegratorTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = SdcQuadrature()
        self._data_3 = [Scalar1D(1.0), Scalar1D(1.0), Scalar1D(1.0)]
        self._data_5 = [Scalar1D(1.0), Scalar1D(1.0), Scalar1D(1.0), Scalar1D(1.0), Scalar1D(1.0)]

    def test_s_and_q_matrix_computation_default_interval(self):
        self._default.init(num_nodes=3)
        computed_smat = self._default._smat
        expected_smat = numpy.array(
            [
                [0.416666666666667, 0.666666666666667, -0.0833333333333335],
                [-0.0833333333333333, 0.666666666666667, 0.416666666666667]
            ]
        )
        self.assertNumpyArrayAlmostEqual(computed_smat, expected_smat)

    def test_q_matrix_computation_default_interval(self):
        self._default.init(num_nodes=3)
        computed_qmat = self._default._qmat
        expected_qmat = numpy.array(
            [
                [0.0, 0.0, 0.0],
                [0.416666666666667, 0.666666666666667, -0.0833333333333335],
                [float(1.0/3.0), float(4.0/3.0), float(1.0/3.0)]
            ]
        )
        self.assertNumpyArrayAlmostEqual(computed_qmat, expected_qmat)

    def test_s_matrix_computation_0_to_1_interval(self):
        self._default.init(num_nodes=3, interval=numpy.array([0.0, 1.0]))
        self.assertNumpyArrayEqual(self._default.nodes_type.interval, numpy.array([0.0, 1.0]))
        computed_smat = self._default._smat
        expected_smat = numpy.array(
            [
                [0.208333333333333, 0.333333333333334, -0.0416666666666667],
                [-0.0416666666666667, 0.333333333333333, 0.208333333333333]
            ]
        )
        self.assertNumpyArrayAlmostEqual(computed_smat, expected_smat)

    def test_q_matrix_computation_0_to_1_interval(self):
        self._default.init(num_nodes=3, interval=numpy.array([0.0, 1.0]))
        self.assertNumpyArrayEqual(self._default.nodes_type.interval, numpy.array([0.0, 1.0]))
        computed_qmat = self._default._qmat
        expected_qmat = numpy.array(
            [
                [0.0, 0.0, 0.0],
                [0.208333333333333, 0.333333333333334, -0.0416666666666667],
                [0.166666666666667, 0.666666666666667, 0.1666666666666667]
            ]
        )
        self.assertNumpyArrayAlmostEqual(computed_qmat, expected_qmat)

    def test_integrate_constant(self):
        self._default.init(num_nodes=3, interval=numpy.array([0.0, 1.0]))

        _integral = self._default.apply(self._data_3)
        self.assertEqual(_integral.value, 1.0)

    def test_partial_integrate_constant(self):
        self._default.init(num_nodes=3, interval=numpy.array([0.0, 1.0]))

        _integral = self._default.apply(self._data_3, target_node=1)
        self.assertAlmostEqual(_integral.value, 0.5)

        _integral = self._default.apply(self._data_3, from_node=1, target_node=2)
        self.assertAlmostEqual(_integral.value, 0.5)

        self._default.init(num_nodes=5, interval=numpy.array([0.0, 1.0]))
        _first_node = self._default.apply(self._data_5, target_node=1)
        _integral = self._default.apply(self._data_5, from_node=1, target_node=4)
        self.assertAlmostEqual(_integral.value + _first_node.value, 1.0)

    def test_interval_transform(self):
        self._default.init()
        self.assertNumpyArrayEqual(self._default.nodes_type.interval, GaussLobattoNodes.STANDARD_INTERVAL)
        self._default.transform_interval(None)
        self.assertNumpyArrayEqual(self._default.nodes_type.interval, GaussLobattoNodes.STANDARD_INTERVAL)

        self._default.transform_interval(numpy.array([0.0, 1.0]))
        self.assertNumpyArrayEqual(self._default.nodes_type.interval, numpy.array([0.0, 1.0]))

        self._default.transform_interval(numpy.array([1.0, 2.0]))
        self.assertNumpyArrayEqual(self._default.nodes_type.interval, numpy.array([1.0, 2.0]))


if __name__ == "__main__":
    import unittest
    unittest.main()
