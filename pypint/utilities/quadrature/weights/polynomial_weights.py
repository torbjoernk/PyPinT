# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np
import numpy.polynomial.polynomial as pol

from pypint.utilities.quadrature.weights.abstract_weights import AbstractWeights
from pypint.utilities.assertions import assert_is_instance, assert_condition


class PolynomialWeights(AbstractWeights):
    """Provider for polynomial weight functions.

    Computes weights of given nodes based on a polynomial weight function of the form
    :math:`\\sum_{i=0}^\\infty c_i x^i`.
    By default, all powers have a coefficient of zero.

    Examples
    --------
    >>> from pypint.utilities.quadrature.nodes.gauss_lobatto_nodes import GaussLobattoNodes
    >>> nodes = GaussLobattoNodes(3)
    >>> # To compute the integration weights for a given set of nodes based
    >>> # on the constant weight function 1.0 use:
    >>> # create an instance
    >>> polyWeights = PolynomialWeights(1.0)
    >>> # compute the weights
    >>> polyWeights.compute_weights(nodes)
    >>> # access the weights
    >>> polyWeights.weights
    array([ 0.3333,  1.3333,  0.3333])
    """

    def __init__(self, *args, **kwargs):
        """
        Notes
        -----
        On successful instantiation, :py:meth:`.PolynomialWeights.init` is called with the arguments given to
        the constructor.
        """
        super(PolynomialWeights, self).__init__(*args, **kwargs)
        self._coefficients = np.zeros(0)
        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        """Sets and defines the weights function.

        Parameters
        ----------
        coeffs : :py:class:`numpy.ndarray` or :py:class:`list`
            Array of coefficients of the polynomial.
            The coefficients can also be given as separate arguments.
        """
        super(PolynomialWeights, self).init(*args, **kwargs)
        if len(args) > 0:
            _coeffs = list(args)
        else:
            _coeffs = kwargs.get('coeffs', [1.0])
        self.coefficients = _coeffs

    def compute_weights(self, nodes, interval=None):
        """Computes weights for stored polynomial and given nodes.

        The weights are calculated with help of the Lagrange polynomials

        .. math::

            \\alpha_i = \\int_a^b\\omega (x) \\prod_{j=1,j \\neq i}^{n} \\frac{x-x_j}{x_i-x_j} \\mathrm{d}x

        See Also
        --------
        :py:meth:`.AbstractWeights.compute_weights` : overridden method
        """
        super(PolynomialWeights, self).compute_weights(nodes, interval)

        a = self._interval[0]
        b = self._interval[1]

        n_nodes = nodes.num_nodes
        alpha = np.zeros(n_nodes)

        for j in range(n_nodes):
            selection = list(range(j))
            selection.extend(list(range(j + 1, n_nodes)))
            poly = [1.0]

            for ais in nodes.nodes[selection]:
                # builds Lagrange polynomial p_i
                poly = pol.polymul(poly, [ais / (ais - nodes.nodes[j]), 1 / (nodes.nodes[j] - ais)])

            # computes \int w(x)p_i dx
            poly = pol.polyint(pol.polymul(poly, self._coefficients))
            alpha[j] = pol.polyval(b, poly) - pol.polyval(a, poly)

        del self._interval
        self._weights = alpha

    def add_coefficient(self, coefficient, power):
        """Adds or sets the coefficient :math:`c` of :math:`cx^p` for a specific :math:`p`.

        The polynomial gets automatically extended to hold the new coefficient in case it didn't included the specified
        power previously.
        Unset, but skipped powers have a coefficient of zero by default.

        Parameters
        ----------
        coefficient : :py:class:`float`
            Coefficient :math:`c` of :math:`cx^p`.
        power : :py:class:`int`
             Power :math:`p` of :math:`cx^p`.

        Examples
        --------
        >>> polyWeights = PolynomialWeights()
        >>> # To set the coefficient of x^3 to 3.14 use:
        >>> polyWeights.add_coefficient(3.14, 3)
        >>> # Similar, to set the constant coefficient 42, e.i. 42*x^0, use:
        >>> polyWeights.add_coefficient(42, 0)
        """
        assert_is_instance(power, int, descriptor="Power", checking_obj=self)
        assert_condition(power >= 0, ValueError,
                         message="Power must be zero or positive: NOT %d" % power, checking_obj=self)

        _coeffs = self._coefficients.tolist()
        while len(_coeffs) <= power:
            _coeffs.append(0.0)
        _coeffs[power] = coefficient
        self.coefficients = _coeffs

    @property
    def coefficients(self):
        """Accessor for the polynomial's coefficients.

        To add or alter single coefficients, see :py:meth:`.add_coefficient`.

        Parameters
        ----------
        coefficients : :py:class:`numpy.ndarray`
            Coefficients of the polynomial.

        Returns
        -------
        coefficients : :py:class:`numpy.ndarray`
            Coefficients :math:`c_i` of the polynomial :math:`\\sum_{i=0}^\\infty c_i x^i`.

        Raises
        ------
        ValueError
            If ``coefficients`` is not a :py:class:`numpy.ndarray` *(only Setter)*.
        """
        return self._coefficients

    @coefficients.setter
    def coefficients(self, coefficients):
        assert_is_instance(coefficients, (list, np.ndarray), descriptor="Coefficients", checking_obj=self)
        self._coefficients = np.asarray(coefficients).reshape(-1)

    def lines_for_log(self):
        _lines = super(PolynomialWeights, self).lines_for_log()
        _lines['Type'] = 'Polynomial'
        _lines['Coefficients'] = "%s" % self.coefficients
        return _lines

    def __str__(self):
        _str = super(PolynomialWeights, self).__str__()[0:-1]
        _str += ", coeffs=%s)" % self.coefficients
        return _str

    def __repr__(self):
        _str = super(PolynomialWeights, self).__repr__()[0:-1]
        _str += ", coeffs=%s>" % self.coefficients
        return _str
