# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import warnings

import numpy as np

from pypint.multi_level_providers.transitioners.abstract_transitioner import AbstractTransitioner
from pypint.multi_level_providers.levels.time_level import TimeLevel
from pypint.utilities.math import lagrange_polynome
from pypint.utilities import assert_is_instance, func_name
from pypint.utilities.logging import LOG


class SpaceInvariantTimeTransitioner(AbstractTransitioner):
    """Transition between to time levels without spatial change

    Time transitioning is based on Lagrange polynomials.
    """
    def __init__(self, *args, **kwargs):
        super(SpaceInvariantTimeTransitioner, self).__init__(*args, **kwargs)

    @AbstractTransitioner.coarse_level.setter
    def coarse_level(self, coarse_level):
        super(self.__class__, self.__class__).coarse_level.fset(self, coarse_level)
        assert_is_instance(coarse_level(), TimeLevel, descriptor="Coarse Level", checking_obj=self)
        self._compute_time_prolongation_matrix()
        self._compute_time_restriction_matrix()

    @AbstractTransitioner.fine_level.setter
    def fine_level(self, fine_level):
        super(self.__class__, self.__class__).fine_level.fset(self, fine_level)
        assert_is_instance(fine_level(), TimeLevel, descriptor="Fine Level", checking_obj=self)
        self._compute_time_prolongation_matrix()
        self._compute_time_restriction_matrix()

    def _prolongate_time(self, coarse_data):
        super(SpaceInvariantTimeTransitioner, self)._prolongate_time(coarse_data)
        _fine = [None] * self.fine_level.num_nodes
        for k in range(0, self.fine_level.num_nodes):
            _fine[k] = coarse_data[0] * self.time_prolongation_operator[k][0]
            for j in range(1, self.coarse_level.num_nodes):
                _fine[k] += coarse_data[j] * self.time_prolongation_operator[k][j]
        return _fine

    def _restrict_time(self, fine_data):
        super(SpaceInvariantTimeTransitioner, self)._restrict_time(fine_data)
        _coarse = [None] * self.coarse_level.num_nodes
        for k in range(0, self.coarse_level.num_nodes):
            _coarse[k] = fine_data[0] * self.time_restriction_operator[k][0]
            for j in range(1, self.fine_level.num_nodes):
                _coarse[k] += fine_data[j] * self.time_restriction_operator[k][j]
        return _coarse

    def _prolongate_space(self, coarse_data):
        super(SpaceInvariantTimeTransitioner, self)._prolongate_space(coarse_data)
        return coarse_data

    def _restrict_space(self, fine_data):
        super(SpaceInvariantTimeTransitioner, self)._restrict_space(fine_data)
        return fine_data

    def _compute_time_prolongation_matrix(self):
        if self.coarse_level is not None and self.fine_level is not None:
            # from here we can assume, that fine_level and coarse_level are available as weakrefs
            self._time_prolongation_operator = np.zeros((self.fine_level.num_nodes, self.coarse_level.num_nodes),
                                                        dtype=float)
            for k in range(0, self.fine_level.num_nodes):
                for j in range(0, self.coarse_level.num_nodes):
                    self._time_prolongation_operator[k][j] = lagrange_polynome(j, self.coarse_level.nodes,
                                                                               self.fine_level.nodes[k])
            # LOG.debug("Prolongation Operator: %s" % self._time_prolongation_operator)
        else:
            warnings.warn("Coarse and/or Fine Level not given but required for computing prolongation operator.")
            LOG.warn("%sCoarse and/or Fine Level not given but required for computing prolongation operator."
                     % func_name(self))

    def _compute_time_restriction_matrix(self):
        if self.coarse_level is not None and self.fine_level is not None:
            # from here we can assume, that fine_level and coarse_level are available as weakrefs
            self._time_restriction_operator = np.zeros((self.coarse_level.num_nodes, self.fine_level.num_nodes),
                                                       dtype=float)
            for k in range(0, self.coarse_level.num_nodes):
                for j in range(0, self.fine_level.num_nodes):
                    self._time_restriction_operator[k][j] = lagrange_polynome(j, self.fine_level.nodes,
                                                                              self.coarse_level.nodes[k])
            # LOG.debug("Restriction Operator: %s" % self._time_restriction_operator)
        else:
            warnings.warn("Coarse and/or Fine Level not given but required for computing restriction operator.")
            LOG.warn("%sCoarse and/or Fine Level not given but required for computing restriction operator."
                     % func_name(self))
