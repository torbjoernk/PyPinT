# coding=utf-8
"""

.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np

from pypint.multi_level_providers.level_transitioners.i_level_transition_provider import ILevelTransitionProvider
from pypint.utilities import assert_condition
from pypint.utilities.logging import LOG


class Injection(ILevelTransitionProvider):
    """Injective restringation and prolongation.

    Injection restringates a fine level with :math:`n` points onto a coarse level with :math:`\\frac{n+1}{2}` points by
    leaving out every other data point.

    On prolongation, injection interpolates a new point between two coarse data points as their arithmetic mean.

    Raises
    ------
    ValueError
        if number of fine level points is even (``fine_level_points``)

    Notes
    -----
    Injective restringation and prolongation only works for a fine level with an odd number of points.
    The coarse level might have an even number of points.

    In addition, injection should only be used when the number of coarse points is a subset of the fine points.
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        assert_condition(kwargs['num_fine_points'] % 2 != 0, ValueError,
                         message="Number of fine level points needs to be odd: %d" % kwargs['num_fine_points'],
                         checking_obj=self)

        self._n_coarse_points = int((self.num_fine_points + 1) / 2)
        self.restringation_operator = np.zeros([self.num_coarse_points, self.num_fine_points])
        self.prolongation_operator = np.zeros([self.num_fine_points, self.num_coarse_points])
        self._construct_transform_matrices()
        LOG.debug("Restringation operator: {}".format(self.restringation_operator))
        LOG.debug("Prolongation operator: {}".format(self.prolongation_operator))

    def prolongate(self, coarse_data):
        super(self.__class__, self).prolongate(coarse_data)
        return np.dot(self.prolongation_operator, coarse_data.transpose()) / 2.0

    def restringate(self, fine_data):
        super(self.__class__, self).restringate(fine_data)
        return np.dot(self.restringation_operator, fine_data.transpose())

    def _construct_transform_matrices(self):
        # construct restringation operator
        for coarse in range(0, self.num_coarse_points):
            fine = (2 * (coarse + 1)) - 2
            self.restringation_operator[coarse][fine] = 1

        # construct prolongation operator
        self.prolongation_operator = \
            self.restringation_operator.copy().transpose()
        for fine in range(0, self.num_fine_points):
            if fine % 2 == 1:
                coarse = int((fine + 1) / 2)
                self.prolongation_operator[fine][coarse - 1] = 1.0
                self.prolongation_operator[fine][coarse] = 1.0
