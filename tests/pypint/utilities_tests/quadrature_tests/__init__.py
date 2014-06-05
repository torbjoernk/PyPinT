# coding=utf-8
import unittest
from nose.tools import *
import numpy

from pypint.utilities.quadrature import QUADRATURE_PRESETS
from pypint.utilities.quadrature.quadrature_base import QuadratureBase


def init_presets(preset):
    integrator = QuadratureBase()
    integrator.init(**preset)
    assert_is_instance(integrator.nodes, numpy.ndarray)
    assert_equal(integrator.nodes.size, preset["num_nodes"])
    assert_is_instance(integrator.weights, numpy.ndarray)
    assert_equal(integrator.weights.size, preset["num_nodes"])


def test_quadrature_presets():
    for preset in QUADRATURE_PRESETS:
        yield init_presets, QUADRATURE_PRESETS[preset]


class IntegratorsTests(unittest.TestSuite):
    def setUp(self):
        pass


if __name__ == "__main__":
    unittest.main()
