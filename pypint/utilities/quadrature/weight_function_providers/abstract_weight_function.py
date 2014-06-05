# coding=utf-8
"""
.. moduleauthor: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

import numpy as np

from pypint.utilities.quadrature.node_providers.abstract_nodes import AbstractNodes
from pypint.utilities.abc import Deepcopyable
from pypint.utilities.assertions import assert_is_instance, assert_condition
from pypint.utilities.tracing import class_name


class AbstractWeightFunction(Deepcopyable, metaclass=ABCMeta):
    """Provider for integration weights functions.

    This is an abstract interface for providers of integration weights functions.
    """
    def __init__(self, *args, **kwargs):
        self._weights = None
        self._interval = None

    @abstractmethod
    def init(self, *args, **kwargs):
        """Sets and defines the weights function.
        """
        pass

    @abstractmethod
    def compute_weights(self, nodes, interval=None):
        """Computes weights for given nodes based on set weight function.

        Parameters
        ----------
        nodes : :py:class:`.AbstractNodes`
            Nodes to compute weights for.

        interval : :py:class:`numpy.ndarray` or :py:class:`None`
            Array with the interval boundaries.
            If :py:class:`None` the boundaries of the given nodes are used.

        Returns
        -------
        computed weights : :py:class:`numpy.ndarray`
            Vector of computed weights.

        Raises
        ------
        ValueError

            * if ``nodes`` is not a :py:class:`.AbstractNodes`
            * if not at least one node is stored in ``nodes`` (i.e. :py:attr:`.AbstractNodes.num_nodes`)
        """
        assert_is_instance(nodes, AbstractNodes, descriptor="Nodes", checking_obj=self)
        assert_condition(nodes.num_nodes > 0,
                         ValueError, message="At least one node must be available.", checking_obj=self)
        if interval is None:
            self._interval = nodes.interval
        else:
            self._interval = interval

    @property
    def weights(self):
        """Accessor for cached computed weights.

        Returns
        -------
        computed weights : :py:class:`numpy.ndarray`
            Cached computed weights.
        """
        return self._weights

    def lines_for_log(self):
        _lines = OrderedDict()
        _lines['Type'] = class_name(self)
        _lines['Weights'] = "%s" % self.weights
        return _lines

    def __str__(self):
        return "%s<0x%x>(weights=%s)" % (class_name(self), id(self), self.weights)

    def __repr__(self):
        return "<%s at 0x%x : weights=%r>" % (class_name(self), id(self), self.weights)
