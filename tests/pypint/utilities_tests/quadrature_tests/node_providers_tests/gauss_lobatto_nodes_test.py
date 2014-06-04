# coding=utf-8
import numpy

from pypint.utilities.quadrature.node_providers.abstract_nodes import AbstractNodes
from pypint.utilities.quadrature.node_providers.gauss_lobatto_nodes import GaussLobattoNodes
from tests import NumpyAwareTestCase, assert_numpy_array_almost_equal

GAUSS_LOBATTO_NODES = {
    2: numpy.array([-1.0, 1.0]),
    3: numpy.array([-1.0, 0.0, 1.0]),
    4: numpy.array([-1.0, -numpy.sqrt(1.0 / 5.0), numpy.sqrt(1.0 / 5.0), 1.0]),
    5: numpy.array([-1.0, -numpy.sqrt(3.0 / 7.0), 0.0, numpy.sqrt(3.0 / 7.0), 1.0])
}


def correctness_of_nodes(n_nodes, expected):
    nodes = GaussLobattoNodes(n_nodes=n_nodes)
    assert_numpy_array_almost_equal(nodes.nodes, expected)


def test_correctness_of_nodes():
    for n_nodes in GAUSS_LOBATTO_NODES:
        yield correctness_of_nodes, n_nodes, GAUSS_LOBATTO_NODES[n_nodes]


class GaussLobattoNodesTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = GaussLobattoNodes()

    def test_is_abstract_nodes(self):
        self.assertIsInstance(self._default, AbstractNodes)

    def test_is_named(self):
        self.assertEqual(self._default.name, 'Gauss-Lobatto')

    def test_interval_transformation(self):
        self._default.init(n_nodes=3)
        self.assertNumpyArrayAlmostEqual(self._default.nodes, GAUSS_LOBATTO_NODES[3])
        self._default.interval = numpy.array([0.0, 1.0])
        self._default.interval = GaussLobattoNodes.STANDARD_INTERVAL
        self.assertNumpyArrayAlmostEqual(self._default.nodes, GAUSS_LOBATTO_NODES[3])

        self.setUp()
        self._default.init(n_nodes=3, interval=numpy.array([0.0, 1.0]))
        self._default.interval = GaussLobattoNodes.STANDARD_INTERVAL
        self.assertNumpyArrayAlmostEqual(self._default.nodes, GAUSS_LOBATTO_NODES[3])


if __name__ == "__main__":
    import unittest
    unittest.main()
