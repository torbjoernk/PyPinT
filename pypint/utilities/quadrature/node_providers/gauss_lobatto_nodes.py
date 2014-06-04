# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np
import numpy.polynomial.legendre as legendre_polynomial

from pypint.utilities.quadrature.node_providers.abstract_nodes import AbstractNodes
from pypint.utilities.assertions import assert_condition


class GaussLobattoNodes(AbstractNodes):
    """Provider for Gauss-Lobatto integration nodes with variable count.
    """

    STANDARD_INTERVAL = np.array([-1.0, 1.0])

    def __init__(self, *args, **kwargs):
        super(GaussLobattoNodes, self).__init__(*args, **kwargs)
        self._interval = GaussLobattoNodes.STANDARD_INTERVAL
        if 'n_nodes' in kwargs:
            self.init(kwargs['n_nodes'])

    @AbstractNodes.name.getter
    def name(self):
        super(self.__class__, self.__class__).name.fget(self)
        return 'Gauss-Lobatto'

    def init(self, n_nodes, interval=None):
        """Initializes and computes Gauss-Lobatto nodes.

        Parameters
        ----------
        n_nodes : :py:class:`int`
            The number of desired Gauss-Lobatto nodes

        See Also
        --------
        :py:meth:`.AbstractNodes.init` : overridden method
        """
        super(GaussLobattoNodes, self).init(n_nodes, interval)
        self._compute_nodes()
        if interval is not None:
            self.transform(interval)

    def transform(self, interval):
        super(GaussLobattoNodes, self).transform(interval)
        assert_condition(self._nodes[0] - self._interval[0] <= 1e-16 and self._nodes[-1] - self._interval[1] <= 1e-16,
                         RuntimeError,
                         message="Newly computed nodes do not match new interval: {} NOT IN {}"
                                 .format(self._nodes, self._interval),
                         checking_obj=self)

    def _compute_nodes(self):
        """Computes Gauss-Lobatto integration nodes.

        Calculates the Gauss-Lobatto integration nodes via a root calculation of derivatives of the legendre
        polynomials.
        Note that the precision of float 64 is not guarantied.
        """
        roots = legendre_polynomial.legroots(legendre_polynomial.legder(np.array([0] * (self.num_nodes - 1) + [1],
                                                                                 dtype=np.float64)))
        self._nodes = np.array(np.append([-1.0], np.append(roots, [1.0])),
                               dtype=np.float64)
