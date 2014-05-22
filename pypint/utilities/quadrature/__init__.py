# coding=utf-8
"""Integrators for Iterative Time Solvers

.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
.. moduleauthor:: Dieter Moser <d.moser@fz-juelich.de>
"""
from pypint.utilities.quadrature.node_providers.gauss_lobatto_nodes import GaussLobattoNodes
from pypint.utilities.quadrature.node_providers.gauss_legendre_nodes import GaussLegendreNodes
from pypint.utilities.quadrature.weight_function_providers.polynomial_weight_function import PolynomialWeightFunction


QUADRATURE_PRESETS = {}
"""Useful presets for quadrature.

This dictionary provides useful parameter presets for frequently used quadrature.
Use them as parameters to the constructor of :py:class:`.QuadratureBase`.
Available presets:

**Gauss-Lobatto**
    Classic *Gauss-Lobatto* integrator with constant one polynomial as the weight function.

Examples
--------
>>> quadrature_base_params = QUADRATURE_PRESETS["Gauss-Lobatto"]
"""


QUADRATURE_PRESETS["Gauss-Lobatto"] = {
    "nodes_type": GaussLobattoNodes,
    "weights_function": {
        "class": PolynomialWeightFunction,
        "coeffs": [1.0]
    },
    "num_nodes": 3
}


QUADRATURE_PRESETS["Gauss-Legendre"] = {
    "nodes_type": GaussLegendreNodes,
    "weights_function": {
        "class": PolynomialWeightFunction,
        "coeffs": [1.0]
    },
    "num_nodes": 3
}
