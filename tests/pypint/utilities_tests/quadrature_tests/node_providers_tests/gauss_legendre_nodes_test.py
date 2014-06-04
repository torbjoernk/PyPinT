# coding=utf-8
import numpy

from pypint.utilities.quadrature.node_providers.abstract_nodes import AbstractNodes
from pypint.utilities.quadrature.node_providers.gauss_legendre_nodes import GaussLegendreNodes
from tests import NumpyAwareTestCase, assert_numpy_array_almost_equal


GAUSS_LEGENDRE_NODES = {
    2: numpy.array(
        [
            -numpy.sqrt(1.0 / 3.0),
            numpy.sqrt(1.0 / 3.0)
        ]
    ),
    5: numpy.array(
        [
            -1.0 / 3.0 * numpy.sqrt(5.0 + 2.0 * numpy.sqrt(10.0 / 7.0)),
            -1.0 / 3.0 * numpy.sqrt(5.0 - 2.0 * numpy.sqrt(10.0 / 7.0)),
            0.0,
            1.0 / 3.0 * numpy.sqrt(5.0 - 2.0 * numpy.sqrt(10.0 / 7.0)),
            1.0 / 3.0 * numpy.sqrt(5.0 + 2.0 * numpy.sqrt(10.0 / 7.0))
        ]
    )
}


def correctness_of_nodes(n_nodes, expected):
    nodes = GaussLegendreNodes(n_nodes=n_nodes)
    assert_numpy_array_almost_equal(nodes.nodes, expected)


def test_correctness_of_nodes():
    for n_nodes in GAUSS_LEGENDRE_NODES:
        yield correctness_of_nodes, n_nodes, GAUSS_LEGENDRE_NODES[n_nodes]


class GaussLegendreNodesTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = GaussLegendreNodes()

    def test_is_abstract_nodes(self):
        self.assertIsInstance(self._default, AbstractNodes)

    def test_is_named(self):
        self.assertEqual(self._default.name, 'Gauss-Legendre')

    def test_interval_transformation(self):
        self._default.init(n_nodes=5)
        self.assertNumpyArrayAlmostEqual(self._default.nodes, GAUSS_LEGENDRE_NODES[5])
        self._default.interval = numpy.array([0.0, 1.0])
        self._default.interval = GaussLegendreNodes.STANDARD_INTERVAL
        self.assertNumpyArrayAlmostEqual(self._default.nodes, GAUSS_LEGENDRE_NODES[5])

        self.setUp()
        self._default.init(n_nodes=5, interval=numpy.array([0.0, 1.0]))
        self._default.interval = GaussLegendreNodes.STANDARD_INTERVAL
        self.assertNumpyArrayAlmostEqual(self._default.nodes, GAUSS_LEGENDRE_NODES[5])


if __name__ == "__main__":
    import unittest
    unittest.main()
