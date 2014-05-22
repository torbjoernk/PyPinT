# coding=utf-8
"""
.. moduleauthor: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import unittest
import numpy
from nose.tools import *

from pypint.utilities.quadrature.quadrature_base import QuadratureBase
from pypint.utilities.quadrature import QUADRATURE_PRESETS


def init_with_presets(preset):
    integrator = QuadratureBase()
    integrator.init(**preset)
    assert_is_instance(integrator.nodes, numpy.ndarray)
    assert_equal(integrator.nodes.size, preset["num_nodes"])
    assert_is_instance(integrator.weights, numpy.ndarray)
    assert_equal(integrator.weights.size, preset["num_nodes"])


def test_init_with_presets():
    for preset in QUADRATURE_PRESETS:
        yield init_with_presets, QUADRATURE_PRESETS[preset]


class IntegratorBaseTest(unittest.TestCase):
    def test_initialization(self):
        integrator = QuadratureBase()


if __name__ == "__main__":
    unittest.main()
