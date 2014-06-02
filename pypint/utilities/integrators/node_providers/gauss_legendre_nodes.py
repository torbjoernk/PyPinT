# coding=utf-8
"""

.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np
from scipy import linalg

from pypint.utilities.integrators.node_providers.i_nodes import INodes
from pypint.utilities import assert_condition


class GaussLegendreNodes(INodes):
    """Provider for Gauss-Legendre integration nodes with variable count.
    """

    std_interval = np.array([-1.0, 1.0])
    """Standard integration interval
    """

    def __init__(self):
        super(GaussLegendreNodes, self).__init__()
        self._interval = GaussLegendreNodes.std_interval

    def init(self, n_nodes, interval=None):
        """Initializes and computes Gauss-Legendre nodes.

        Parameters
        ----------
        n_nodes : :py:class:`int`
            The number of desired Gauss-Legendre nodes

        See Also
        --------
        :py:meth:`.INodes.init` : overridden method
        """
        super(GaussLegendreNodes, self).init(n_nodes, interval)
        self.num_nodes = n_nodes
        self._nodes = np.zeros(self.num_nodes)
        self._compute_nodes()
        if interval is not None:
            self.transform(interval)

    @property
    def num_nodes(self):
        """Accessor of number of Gauss-Legendre nodes.

        Raises
        ------
        ValueError
            if ``n_nodes`` is smaller than 2 *(only Setter)*.

        See Also
        --------
        :py:attr:`.INodes.num_nodes` : overridden method
        """
        return super(self.__class__, self.__class__).num_nodes.fget(self)

    @num_nodes.setter
    def num_nodes(self, n_nodes):
        super(self.__class__, self.__class__).num_nodes.fset(self, n_nodes)
        assert_condition(n_nodes >= 1,
                         ValueError, message="Gauss-Legendre with less than one node doesn't make any sense.",
                         checking_obj=self)
        self._num_nodes = n_nodes

    def _compute_nodes(self):
        """Computats nodes for the Gauss-Legendre quadrature of order :math:`n>1` on :math:`[-1,+1]`.

        (ported from MATLAB code, reference see below, original commend from MATLAB code:)

        .. epigraph::

            Unlike many publicly available functions, this function is valid for :math:`n>=46`.
            This is due to the fact that it does not rely on MATLAB's build-in 'root' routines to determine the roots
            of the Legendre polynomial, but finds the roots by looking for the eigenvalues of an alternative version of
            the companion matrix of the n'th degree Legendre polynomial.
            The companion matrix is constructed as a symmetrical matrix, guaranteeing that all the eigenvalues (roots)
            will be real.
            On the contrary, MATLAB's 'roots' function uses a general form for the companion matrix, which becomes
            unstable at higher orders :math:`n`, leading to complex roots.

            -- original MATLAB function by: Geert Van Damme <geert@vandamme-iliano.be> (February 21, 2010)
        """
        # Building the companion matrix comp_mat
        # comp_mat is such that det(nodes*I-comp_mat)=P_n(nodes), with P_n the
        # Legendre polynomial under consideration.
        # Moreover, comp_mat will be constructed in such a way that it is
        # symmetrical.
        linspace = np.linspace(start=1, stop=self.num_nodes - 1,
                               num=self.num_nodes - 1)
        a = linspace / np.sqrt(4.0 * linspace ** 2 - 1.0)
        comp_mat = np.diag(a, 1) + np.diag(a, -1)

        # Determining the abscissas (nodes)
        # - since det(nodesI-comp_mat)=P_n(nodes), the abscissas are the roots
        #   of the characteristic polynomial, i.d. the eigenvalues of comp_mat
        [eig_vals, _] = linalg.eig(comp_mat)
        indizes = np.argsort(eig_vals)
        nodes = eig_vals[indizes]

        self._nodes = nodes.real

    def __str__(self):
        return "GaussLegendreNodes<0x%x>(n=%d, nodes=%s)" % (id(self), self.num_nodes, self.nodes)
