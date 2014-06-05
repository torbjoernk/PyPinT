# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from collections import OrderedDict

import numpy as np

from pypint.utilities.quadrature.nodes.abstract_nodes import AbstractNodes
from pypint.utilities.quadrature.weights.abstract_weights import AbstractWeights
from pypint.utilities.data_structures.abstract_spatial_object import AbstractSpatialObject
from pypint.utilities.abc import Deepcopyable
from pypint.utilities.assertions import assert_is_instance, assert_condition, class_name


class QuadratureBase(Deepcopyable):
    """Basic and generic integrator for variable nodes and weights.
    """
    def __init__(self, *args, **kwargs):
        self._nodes = None
        self._weights_function = None

    def init(self, *args, **kwargs):
        """Initializes the integrator with given nodes and weights function.

        Before setting the given attributes, a consistency check is carried out testing for the correct types.
        :py:meth:`.AbstractNodes.init` is called on the provided nodes object.
        :py:meth:`.AbstractWeights.compute_weights` is called on the provided weight function object.

        Parameters
        ----------
        nodes_type : :py:class:`.AbstractNodes`
            Type of integration nodes as the class name **not instance**.
        num_nodes : :py:class:`int`
            Number of integration nodes
        weights_function : :py:class:`.AbstractWeights` or :py:class:`dict`
            Weight function for the integration nodes.
            If it is a dictionary, it must have a ``type`` field with the :py:class:`.AbstractWeights` as the value.
            Further fields are used as parameters to :py:class:`.AbstractWeights.init`.
            In both cases the weight function type must be given as a name **not instance**.

        Raises
        ------
        ValueError :
            If the type of one of the given arguments does not match.

            * ``nodes_type`` must be a subclass of :py:class:`.AbstractNodes`
            * ``num_nodes`` must be an :py:class:`int`
            * ``weights_function`` must be a subclass of :py:class:`.AbstractWeights` or :py:class:`dict`

                - if ``weights_function`` is a dictionary, its field ``type`` must be a subclass of
                  :py:class:`.AbstractWeights`.

        Examples
        --------
        >>> from pypint.utilities.quadrature import QUADRATURE_PRESETS
        >>> integrator = QuadratureBase()
        >>> # create classic Gauss-Lobatto integrator with 4 integration nodes
        >>> options = QUADRATURE_PRESETS['Gauss-Lobatto']
        >>> options['num_nodes'] = 4
        >>> integrator.init(**options)
        """
        nodes_type = kwargs.get('nodes_type')
        num_nodes = kwargs.get('num_nodes')
        weights_function = kwargs.get('weights_function')
        interval = kwargs.get('interval')

        assert_condition(isinstance(nodes_type, type) and issubclass(nodes_type, AbstractNodes),
                         ValueError, message="Given Nodes are of incompatible type: NOT %s"
                                             % [b.__name__ for b in nodes_type.__bases__],
                         checking_obj=self)
        if isinstance(weights_function, dict):
            assert_condition('type' in weights_function and isinstance(weights_function['type'], type)
                             and issubclass(weights_function['type'], AbstractWeights),
                             ValueError, "Given Weights Function is of incompatible type: NOT %s"
                                         % [b.__name__ for b in weights_function['type'].__bases__],
                             checking_obj=self)
            self._weights_function = weights_function['type']()
            # copy() is necessary as dictionaries are passed by reference
            _weight_function_options = weights_function.copy()
            del _weight_function_options['type']
            self.weights_function.init(**_weight_function_options)
        else:
            assert_condition(issubclass(weights_function, AbstractWeights),
                             ValueError, message="Given Weight Function is of incompatible type: NOT %s"
                                                 % [b.__name__ for b in weights_function.__bases__],
                             checking_obj=self)
            self._weights_function = weights_function()
            self.weights_function.init()
        assert_is_instance(num_nodes, int,
                           "Number of nodes need to be an integer: NOT %s" % type(num_nodes),
                           checking_obj=self)
        self._nodes = nodes_type()
        self.nodes_type.init(num_nodes, interval=interval)
        self.weights_function.compute_weights(self.nodes_type, interval=self.nodes_type.interval)

    def apply(self, data, **kwargs):
        """Applies this integrator to given data.

        Parameters
        ----------
        data : :py:class:`numpy.ndarray` or :py:class:`list` of :py:class:`.AbstractSpatialObject`
            Data vector of the values at given time points.
            Its length must equal the number of integration nodes.

        Raises
        ------
        ValueError :
            If ``data`` is not a :py:class:`numpy.ndarray` or :py:class:`list` of :py:class:`.AbstractSpatialObject` and
            has not as many items as there are integration nodes provided by :py:attr:`.nodes`.
        """
        assert_is_instance(data, (list, np.ndarray), descriptor="Data to integrate", checking_obj=self)
        assert_condition(len(data) == self.num_nodes, ValueError,
                         message="Number of Integration Data Points does not match number of Nodes", checking_obj=self)
        assert_condition(all(isinstance(elem, AbstractSpatialObject) for elem in data),
                         ValueError, message="Data to Integrate must be a list of Spatial Objects.",
                         checking_obj=self)

    def transform_interval(self, interval):
        """Transform current interval to the given one

        The integration nodes are transformed to fit the given interval and subsequently the weights are recomputed to
        match the new nodes.

        See Also
        --------
        :py:meth:`.AbstractNodes.transform` : method called for node transformation
        """
        if interval is not None:
            self.nodes_type.interval = interval
        self.weights_function.compute_weights(self.nodes_type)

    @property
    def nodes(self):
        """Proxy accessor for the integration nodes.

        See Also
        --------
        :py:attr:`.AbstractNodes.nodes`
        """
        return self.nodes_type.nodes if self.nodes_type else None

    @property
    def num_nodes(self):
        return self.nodes_type.num_nodes if self.nodes_type else None

    @property
    def weights(self):
        """Proxy accessor for the calculated and cached integration weights.

        See Also
        --------
        :py:attr:`.AbstractWeights.weights`
        """
        return self.weights_function.weights if  self.weights_function else None

    @property
    def nodes_type(self):
        """Read-only accessor for the type of nodes

        Returns
        -------
        nodes : :py:class:`.AbstractNodes`
        """
        return self._nodes

    @property
    def weights_function(self):
        """Read-only accessor for the weights function

        Returns
        -------
        weights_function : :py:class:`.AbstractWeights`
        """
        return self._weights_function

    def lines_for_log(self):
        _lines = OrderedDict()
        _lines['Nodes'] = \
            self._nodes.print_lines_for_log() if self._nodes is not None else 'na'
        _lines['Weights Function'] = \
            self._weights_function.print_lines_for_log() if self._weights_function is not None else 'na'
        return _lines

    def __str__(self):
        return \
            "%s<0x%x>(nodes=%s, weights=%s)" \
            % (class_name(self), id(self), self.nodes_type, self.weights_function)

    def __repr__(self):
        return \
            "<%s at 0x%x : nodes=%r, weights=%r>" \
            % (class_name(self), id(self), self.nodes_type, self.weights_function)
