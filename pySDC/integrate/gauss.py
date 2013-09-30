import numpy as np
from scipy import linalg
import itertools
import pySDC.globals as Config
from pySDC.integrate.quadrature import Quadrature


class Gauss(Quadrature):
    """
    """

    def __init__(self):
        """
        """
        super(Quadrature, self).__init__()

    @staticmethod
    def integrate(func=lambda t, x: 1.0, vals=None, begin=0, end=1, n=3, t=1.0, partial=None,
                  method="legendre"):
        """
        integrates given function in [begin, end] using n points at time t with method 'method'
        """
        _a = begin
        _b = end

        if _a == _b or (_b - _a) <= 0.0:
            raise ValueError("Integration interval must be non-zero positive (end - begin = {: f})."
                             .format(_b - _a))

        _nw = {'nodes': [], 'weights': []}
        if method == "lobatto" and partial is not None:
            n = len(vals)
            _nw['nodes'] = Gauss.lobatto_nodes(n)
        else:
            _nw = Gauss.get_nodes_and_weights(n, method)

        _trans = Gauss.transform(_a, _b)

        if vals is not None:
            assert len(vals) == len(_nw['nodes']), \
                "Number of given values ({:d}) not matching number of integration points ({:d})."\
                .format(len(vals), len(_nw['nodes']))

        _result = {'full': 0.0, 'partial': 0.0}
        _count_terms = 0

        if partial is not None:
            _smat = Gauss.build_s_matrix(_trans[0] * _nw['nodes'] + [_trans[1]] * len(_nw['nodes']), begin, end, method)
            Config.LOG.debug("Constructed Smat:\n{}".format(str(_smat)))

        if partial is None:
            for i in range(0, len(_nw['nodes'])):
                if func is not None:
                    _result['full'] += _nw['weights'][i] * func(t, _trans[0] * _nw['nodes'][i] + _trans[1])
                elif vals is not None:
                    _result['full'] += _nw['weights'][i] * vals[i]
                else:
                    raise ValueError("Either func or vals must be given.")
                _count_terms += 1
        elif vals is not None:
            Config.LOG.debug("using _smat row {:d}:".format(partial - 1) + str(_smat[partial - 1]))
            assert len(_smat[partial - 1]) == len(vals), \
                "_smat entries ({:d}) not matching values ({:d})"\
                .format(len(_smat[partial - 1]), len(vals))
            for i in range(0, len(_smat[partial - 1])):
                _result['partial'] += _smat[partial - 1][i] * vals[i]
                Config.LOG.debug("   {: f} += {: f} * {: f}"
                                 .format(_result['partial'], _smat[partial - 1][i], vals[i]))
                _count_terms += 1
        else:
            raise NotImplementedError("Not yet implemented")

        assert _count_terms > 0, \
            "Nothing was integrated (begin={:f}, end={:f}, n={:d}, partial={:d})."\
            .format(begin, end, n, partial)

        _result['full'] *= _trans[0]
        _result['partial'] *= _trans[0]

        if partial is not None:
            Config.LOG.debug("integrated on [{: f},{: f}] as partial interval in [{: f}, {: f}]"
                             .format(_trans[0] * _nw['nodes'][begin] + _trans[1],
                                     _trans[0] * _nw['nodes'][partial] + _trans[1], begin, end))
            Config.LOG.debug("used values: {}".format(str(vals)))
            Config.LOG.debug("n nodes: {:d}".format(_count_terms))
            return _result['partial']
        else:
            return _result['full']

    @staticmethod
    def get_nodes_and_weights(n, method="legendre"):
        """
        returns integration nodes and weights for given type and number of points
        """
        if method == "legendre":
            return Gauss.legendre_nodes_and_weights(n)
        elif method == "lobatto":
            return Gauss.lobatto_nodes_and_weights(n)
        else:
            raise NotImplementedError("Gaus-{}-Quadrature not implemented/known.".format(method))

    @staticmethod
    def transform(a, b):
        """
        calculates transformation coefficients to map [a,b] to [-1,1]

        see: http://en.wikipedia.org/wiki/Gaussian_quadrature#Change_of_interval
        """
#         print('[{: f}, {: f}]: {: f}, {: f}'.format(a, b, (b-a)/2.0, (b+a)/2.0))
        return [(b - a) / 2.0, (b + a) / 2.0]

    @staticmethod
    def build_s_matrix(nodes, begin, end, method):
        """
        :param nodes:
        :param begin:
        :param end:
        :param method:
        :return:
        """
        n = len(nodes)

        if method == "lobatto":
            smat = np.zeros((n - 1, n), dtype=float)
            for i in range(1, n):
                smat[i - 1] = Gauss.compute_weights(nodes, nodes[i - 1], nodes[i])
        elif method == "legendre":
            smat = np.zeros((n + 1, n), dtype=float)
            smat[0] = Gauss.compute_weights(nodes, begin, nodes[0])
            for i in range(1, n):
                smat[i] = Gauss.compute_weights(nodes, nodes[i - 1], nodes[i])
            smat[n] = Gauss.compute_weights(nodes, nodes[n - 1], end)
        else:
            raise (ValueError, "Constructing S-Matrix for method '{}' not implemented."
                               .format(method))

        return smat

    @staticmethod
    def legendre_nodes_and_weights(n):
        """
        computats nodes and weights for the Gauss-Legendre quadrature of order n>1 on [-1, +1]
        (ported from MATLAB code, reference see below)

        (original comment from MatLab source; modified)
        Unlike many publicly available functions, this function is valid for
        n>=46.
        This is due to the fact that it does not rely on MATLAB's build-in 'root'
        routines to determine the roots of the Legendre polynomial, but finds the
        roots by looking for the eigenvalues of an alternative version of the
        companion matrix of the n'th degree Legendre polynomial.
        The companion matrix is constructed as a symmetrical matrix, guaranteeing
        that all the eigenvalues (roots) will be real.
        On the contrary, MATLAB's 'roots' function uses a general form for the
        companion matrix, which becomes unstable at higher orders n, leading to
        complex roots.

        (Credit, where credit due)
        original MATLAB function by: Geert Van Damme <geert@vandamme-iliano.be> (February 21, 2010)
        """
        if n < 2:
            raise ValueError("Gauss-Legendre quadrature does not work with less than three points.")

        # Building the companion matrix cm
        # cm is such that det(xI-cm)=P_n(x), with P_n the Legendre polynomial
        # under consideration. Moreover, cm will be constructed in such a way
        # that it is symmetrical.
        j = np.linspace(start=1, stop=n - 1, num=n - 1)
        a = j / np.sqrt(4.0 * j ** 2 - 1.0)
        cm = np.diag(a, 1) + np.diag(a, -1)

        # Determining the abscissas (x) and weights (w)
        # - since det(xI-cm)=P_n(x), the abscissas are the roots of the
        #   characteristic polynomial, i.d. the eigenvalues of cm;
        # - the weights can be derived from the corresponding eigenvectors.
        [l, v] = linalg.eig(cm)
        ind = np.argsort(l)
        x = l[ind]
        v = v[:, ind].transpose()
        w = 2.0 * np.asarray(v[:, 0]) ** 2.0

        #print("Gauss.legendre_nodes_and_weights({:d})={: f}".format(n, np.around(x.real, Config.DIGITS)))
        return {'nodes': np.around(x.real, Config.DIGITS),
                'weights': np.around(w.real, Config.DIGITS)}

    @staticmethod
    def lobatto_nodes_and_weights(n):
        """
        Gauss-Lobatto nodes and weights for 3 to 5 integration points (hard coded)

        source of values: http://en.wikipedia.org/wiki/Gaussian_quadrature#Gauss.E2.80.93Lobatto_rules
        """
        if n == 3:
            return {'nodes': [-1.0,
                              0.0,
                              1.0],
                    'weights': [1.0 / 3.0,
                                4.0 / 3.0,
                                1.0 / 3.0]}
        elif n == 4:
            return {'nodes': [-1.0,
                              -1.0 / 5.0 * np.sqrt(5),
                              1.0 / 5.0 * np.sqrt(5),
                              1.0],
                    'weights': [1.0 / 6.0,
                                5.0 / 6.0,
                                5.0 / 6.0,
                                1.0 / 6.0]}
        elif n == 5:
            return {'nodes': [-1.0,
                              -1.0 / 7.0 * np.sqrt(21),
                              0.0,
                              1.0 / 7.0 * np.sqrt(21),
                              1.0],
                    'weights': [1.0 / 10.0,
                                49.0 / 90.0,
                                32.0 / 45.0,
                                49.0 / 90.0,
                                1.0 / 10.0]}
        elif n < 3:
            raise ValueError("Gauss-Lobatto quadrature does not work with less than three points.")
        else:
            raise NotImplementedError("Gauss-Lobatto with {:d} is not implemented yet.".format(n))

    @staticmethod
    def lobatto_nodes(n):
        """
        Compute n nodes and weights with a fix start [-1,1]

        :param n:
        :return:
        """
        j = np.arange(1, n + 1)
        a = (2.0 * j - 1.0) / j
        c = (j - 1.0) / j

        j = np.diag(1 / (a[0:n-1]), 1) + np.diag(c[1:n+1] / a[1:n+1], -1)
        # magic trick . . .
        j[n-1, n-2] = 1.0

        # ... no magic actually just the following consideration
        #   1.      p_j(-1)=(-1)^j
        #       and p_j(1) =1
        #
        #   2. p_j(x)=(a_j * x )p_j-1(x)-c_j p_j-2(x)
        #      we expect that the roots of p_j are the quadrature nodes
        #      0= p_j(-1) = a_j * (-1)*(-1)^(j-1)-c_j*(-1)^(j-2)
        # <=>  a_j=c_j
        #   3. for x=1 we get the same
        #      that means we have automatically the roots 1 and -1
        #      in this case GaussRadau equiv GaussLobatto
        #      note 1: this calculations only work for the quadrature weight w(x)=1
        #      note 2: this ist not the symmetrical form like in GaussLegendre,
        #              hence it is less stable
        #      note 3: the computed weights are useless (and thus not computed here)
        [l, v] = linalg.eig(j)
        ind = np.argsort(l)
        x = l[ind]
        return x.real

    @staticmethod
    def compute_weights(nodes, begin, end):
        """
        :param nodes:
        :param begin:
        :param end:
        :return:
        """
        n = len(nodes)
        weights = np.zeros(n, dtype=float)
        for i in range(0, n):
            selection = itertools.chain(range(0, i), range(i + 1, n))
            #print("selection: {}".format(Gauss.print_iterable(selection)))
            poly = [1]
            for ar in selection:
                poly = np.polymul(poly, [1.0 / (nodes[i] - nodes[ar]),
                                         (1.0 * nodes[ar]) / (nodes[ar] - nodes[i])])
            poly = np.polyint(poly)
            weights[i] = np.polyval(poly, end) - np.polyval(poly, begin)
        return weights

    @staticmethod
    def print_iterable(iterable):
        string = "[ "
        for elem in iterable:
            string += str(elem) + " "
        string += "]"
        return string
