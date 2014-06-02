# coding=utf-8
"""
.. moduleauthor: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""

import numpy
from nose.tools import *

from pypint.utilities.integrators.integrator_base import IntegratorBase
from pypint.utilities.integrators import INTEGRATOR_PRESETS


def init_with_presets(preset):
    integrator = IntegratorBase()
    integrator.init(**preset)
    assert_is_instance(integrator.nodes, numpy.ndarray)
    assert_equal(integrator.nodes.size, preset["num_nodes"])
    assert_is_instance(integrator.weights, numpy.ndarray)
    assert_equal(integrator.weights.size, preset["num_nodes"])


def test_init_with_presets():
    for preset in INTEGRATOR_PRESETS:
        yield init_with_presets, INTEGRATOR_PRESETS[preset]


class IntegratorBaseTest(unittest.TestCase):
    def test_initialization(self):
        integrator = IntegratorBase()


if __name__ == "__main__":
    unittest.main()
