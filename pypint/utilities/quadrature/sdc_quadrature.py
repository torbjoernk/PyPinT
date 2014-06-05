# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np

from pypint.utilities.quadrature.quadrature_base import QuadratureBase
from pypint.utilities.quadrature.nodes.gauss_lobatto_nodes import GaussLobattoNodes
from pypint.utilities.quadrature.weights.polynomial_weights import PolynomialWeights
from pypint.utilities.assertions import assert_is_instance, assert_condition
from pypint.utilities.logging import LOG


class SdcQuadrature(QuadratureBase):
    """Integral part of the SDC algorithm.
    """
    def __init__(self, *args, **kwargs):
        super(SdcQuadrature, self).__init__(*args, **kwargs)
        self._smat = np.zeros(0)
        self._qmat = np.zeros(0)

    def init(self, *args, **kwargs):
        """Initialize SDC Integrator

        Parameters
        ----------
        nodes_type : :py:class:`.AbstractNodes`
            type of the nodes
            (defaults to :py:class:`.GaussLobattoNodes`)

        num_nodes : :py:class:`int`
            number of nodes
            (defaults to 3)

        weights_function : :py:class:`.AbstractWeights`
            type of the weights function
            (defaults to :py:class:`.PolynomialWeights`)

        interval : :py:class:`numpy.ndarray` or :py:class:`None`
            interval for the nodes
            (see :py:meth:`.AbstractNodes.transform` for possible values)
        """
        if 'nodes_type' not in kwargs:
            kwargs['nodes_type'] = GaussLobattoNodes
        if 'num_nodes' not in kwargs:
            kwargs['num_nodes'] = 3
        if 'weights_function' not in kwargs:
            kwargs['weights_function'] = PolynomialWeights
        super(SdcQuadrature, self).init(*args, **kwargs)
        self._construct_s_matrix()

    def apply(self, data, **kwargs):
        """Computes the integral until the given node from the previous one.

        For integration nodes :math:`\\tau_i`, :math:`i=1,\\dots,n` specifying :math:`\\tau_3` as ``target_node``
        results in the integral :math:`\\int_{\\tau_2}^{\\tau_3}`.

        Examples
        --------
        Given five integration nodes: :math:`\\tau_1, \\dots, \\tau_5`.

        To compute the integral from :math:`\\tau_2` to :math:`\\tau_3` one need to specify ``target_node`` as ``3`` and
        ``from_node`` as ``2``.
        Internally, the :math:`S`-matrix is used.

        To compute the full integral over all nodes one need to specify ``target_node`` as ``5`` only.
        Internally, the :math:`Q`-matrix is used.

        Parameters
        ----------
        target_node : :py:class:`int`
            *(optional)*
            (0-based) index of the last node to integrate.
            In case it is not given, an integral over the full interval is assumed.

        from_node : :py:class:`int`
            *(optional)*
            (0-based) index of the first node to integrate from.
            *(defaults to ``0``)*

        Raises
        ------
        ValueError

            * if ``target_node`` is not given
            * if ``from_node`` is not smaller than ``target_node``

        See Also
        --------
        :py:meth:`.QuadratureBase.apply` : overridden method
        """
        _target_index = kwargs.get('target_node', self._qmat.shape[0] - 1)
        assert_is_instance(_target_index, int, descriptor="Target Node Index", checking_obj=self)

        _from_index = kwargs.get('from_node', 0)
        assert_is_instance(_from_index, int, descriptor="From Node Index", checking_obj=self)

        assert_condition(_from_index < _target_index,
                         ValueError,
                         message="Integration must cover at least two nodes: %d !< %d" % (_from_index, _target_index),
                         checking_obj=self)

        super(SdcQuadrature, self).apply(data)

        _integral = data[0].__class__()

        if _from_index != 0:
            assert_condition(_target_index <= self._smat.shape[0],
                             ValueError, message="Target Node Index %d too large. Must be within [%d, %d)"
                                                 % (_target_index, 1, self._smat.shape[0]),
                             checking_obj=self)
            if _from_index < _target_index - 1:
                for _subfrom in range(_from_index, _target_index):
                    _integral += self.apply(data, from_node=_subfrom, target_node=_subfrom + 1)
            else:
                # LOG.debug("Integrating from node {:d} to {:d} with S-Mat row {:d} on interval {}."
                #           .format(_from_index, _target_index, _target_index - 1, self.nodes_type.interval))
                # LOG.debug("  data:    %s" % data.flatten())
                # LOG.debug("  weights: %s" % self._smat[_target_index - 1])
                for _node_index in range(self.num_nodes):
                    _integral += data[_node_index] * self._smat[_target_index - 1][_node_index]
        else:
            assert_condition(_target_index < self._qmat.shape[0],
                             ValueError, message="Target Node Index %d too large. Must be within [%d, %d]"
                                                 % (_target_index, 1, self._qmat.shape[0]),
                             checking_obj=self)
            # LOG.debug("Integrating up to node {:d} with Q-Mat row {:d} on interval {}."
            #           .format(_target_index, _target_index, self.nodes_type.interval))
            # LOG.debug("  data:    %s" % data.flatten())
            # LOG.debug("  weights: %s" % self._qmat[_target_index])
            for _node_index in range(self.num_nodes):
                _integral += data[_node_index] * self._qmat[_target_index][_node_index]

        return _integral

    def transform_interval(self, interval):
        """Transforms nodes onto new interval

        See Also
        --------
        :py:meth:`.QuadratureBase.transform_interval` : overridden method
        """
        if interval is not None:
            if interval[1] - interval[0] != self.nodes[-1] - self.nodes[0]:
                LOG.debug("Size of interval changed. Recalculating weights.")
                super(SdcQuadrature, self).transform_interval(interval)
                self._construct_s_matrix()
            else:
                super(SdcQuadrature, self).transform_interval(interval)
                LOG.debug("Size of interval did not change. Don't need to recompute S and Q matrices")
        else:
            LOG.debug("Cannot transform interval to None. Skipping.")

    def _construct_s_matrix(self):
        """Constructs integration :math:`S`-matrix

        Rows of the matrix are the integration from one node to the next.
        I.e. row :math:`i` integrates from node :math:`i-1` to node :math:`i`.
        """
        assert_is_instance(self._nodes, GaussLobattoNodes,
                           message="Other than Gauss-Lobatto integration nodes not yet supported.", checking_obj=self)
        self._smat = np.zeros((self.nodes.size - 1, self.nodes.size), dtype=float)
        for i in range(1, self.nodes.size):
            self.weights_function.compute_weights(self.nodes_type, np.array([self.nodes[i - 1], self.nodes[i]]))
            self._smat[i - 1] = self.weights_function.weights

        # compute Q-matrix
        self._construct_q_matrix()

    def _construct_q_matrix(self):
        """Constructs integration :math:`Q`-matrix

        The :math:`Q`-matrix is the commulation of the rows of the :math:`S`-matrix.
        I.e. row :math:`i` of :math:`Q` is the sum of the rows :math:`0` to :math:`i - 1` of :math:`S`.

        However, :math:`Q` has one row more than :math:`S`, namely the first, which is constant zero.
        """
        self._qmat = np.zeros((self.nodes.size, self.nodes.size), dtype=float)
        for i in range(0, self._smat.shape[0]):
            self._qmat[i + 1] = self._qmat[i] + self._smat[i]
