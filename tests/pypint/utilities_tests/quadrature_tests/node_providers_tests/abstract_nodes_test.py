# coding=utf-8
from nose.tools import *
import numpy

from tests import NumpyAwareTestCase, assert_numpy_array_equal
from pypint.utilities.quadrature.node_providers.abstract_nodes import AbstractNodes


class NodesImplementation(AbstractNodes):
    def __init__(self, *args, **kwargs):
        super(NodesImplementation, self).__init__(*args, **kwargs)

    @AbstractNodes.name.getter
    def name(self):
        super(self.__class__, self.__class__).name.fget(self)
        return 'Dummy Implementation'

    def init(self, n_nodes, interval=None):
        super(NodesImplementation, self).init(n_nodes, interval=interval)


test_data = [
    {
        'from': {
            'interval': [-1.0, 1.0],
            'nodes': [-1.0, 0.0, 1.0]
        },
        'to': {
            'interval': [0.0, 0.5],
            'nodes': [0.0, 0.25, 0.5]
        }
    },
    {
        'from': {
            'interval': [0.0, 0.5],
            'nodes': [0.0, 0.25, 0.5]
        },
        'to': {
            'interval': [0.5, 1.0],
            'nodes': [0.5, 0.75, 1.0]
        }
    }
]


def transform_nodes(from_data, to_data):
    _nodes = NodesImplementation()
    _nodes._interval = numpy.array(from_data['interval'])
    _nodes._nodes = numpy.array(from_data['nodes'])
    _nodes.transform(numpy.array(to_data['interval']))
    assert_equal(_nodes.nodes[0], to_data['interval'][0])
    assert_equal(_nodes.nodes[-1], to_data['interval'][1])
    assert_numpy_array_equal(_nodes.nodes, numpy.array(to_data['nodes']))


def test_interval_transformation():
    for data_set in test_data:
        yield transform_nodes, data_set['from'], data_set['to']


class AbstractNodesTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = NodesImplementation()

    def test_provides_initialization_method(self):
        self.assertEqual(self._default.num_nodes, 0)
        self._default.init(3)

    def test_provides_accessors_for_nodes(self):
        self.assertEqual(self._default.num_nodes, 0)
        self.assertNumpyArrayEqual(self._default.nodes, numpy.zeros(0))

    def test_provides_interval_accessor(self):
        self.assertNumpyArrayEqual(self._default.interval, numpy.array([0.0, 0.0]))

    def test_provides_stringification(self):
        self.assertRegex(str(self._default), '^NodesImplementation<0x[0-9a-f]*>\(n=0, nodes=\[\]\)$')
        self.assertRegex(repr(self._default), '^<NodesImplementation at 0x[0-9a-f]* : n=0, nodes=\[\]>$')
        self.assertIsNotNone(self._default.lines_for_log())
        self.assertIn('Type', self._default.lines_for_log())
        self.assertIn('Number Nodes', self._default.lines_for_log())


if __name__ == '__main__':
    import unittest
    unittest.main()
