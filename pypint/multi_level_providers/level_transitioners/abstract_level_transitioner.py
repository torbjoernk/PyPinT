# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from weakref import ReferenceType

from pypint.multi_level_providers.levels.abstract_level import AbstractLevel
from pypint.utilities import assert_is_instance, assert_condition, class_name


class AbstractLevelTransitioner(object, metaclass=ABCMeta):
    """Interface for level transitioners.
    """

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        coarse_level :
            *(optional)*
            Coarse Level; see :py:attr:`.coarse_level` for details
        fine_level :
            *(optional)*
            Fine Level; see :py:attr:`.fine_level` for details
        """
        self._coarse_level = None
        self._fine_level = None

        self._time_prolongation_operator = None
        self._spatial_prolongation_operator = None
        self._time_restriction_operator = None
        self._spatial_restriction_operator = None

        if 'coarse_level' in kwargs:
            self.coarse_level = kwargs['coarse_level']
        if 'fine_level' in kwargs:
            self.fine_level = kwargs['fine_level']

    def prolongate(self, coarse_data):
        """Prolongates given data from the coarse to the fine level in space and time.

        The prolongation is carried out first in time and then in space.
        Override this method to change the order.

        Parameters
        ----------
        coarse_data :
            coarse data to prolongate

        Returns
        -------
        prolongated_data :
            Space-Time prolongated data on the fine level.

        Raises
        ------
        ValueError
            If ``coarse_data`` is incompatible to :py:attr:`.coarse_level` or prolongated space-time data is not
            compatible with :py:attr:`.fine_level`.
        """
        assert_condition(self.coarse_level is not None and self.coarse_level.validate_data(coarse_data),
                         ValueError, message="Coarse Data is incompatible to Coarse Level: %s" % coarse_data,
                         checking_obj=self)

        fine_time_data = self._prolongate_time(coarse_data)
        fine_space_time_data = self._prolongate_space(fine_time_data)

        assert_condition(self.fine_level is not None and self.fine_level.validate_data(fine_space_time_data),
                         ValueError, message="Prolongated Space-Time Data is incompatible to Fine Level: %s"
                                             % fine_space_time_data,
                         checking_obj=self)
        return fine_space_time_data

    def restrict(self, fine_data):
        """Restricts given data from the fine to the coarse level in space and time.

        The restriction is carried out first in time and then in space.
        Override this method to change the order.

        Parameters
        ----------
        fine_data :
            fine data to restrict

        Returns
        -------
        restricted_data :
            Space-Time restricted data on the coarse level.

        Raises
        ------
        ValueError
            If ``fine_data`` is incompatible to :py:attr:`.fine_level` or restricted space-time data is not compatible
            with :py:attr:`.coarse_level`.
        """
        assert_condition(self.fine_level is not None and self.fine_level.validate_data(fine_data),
                         ValueError, message="Fine Data is incompatible to Fine Level: %s" % fine_data,
                         checking_obj=self)

        coarse_time_data = self._restrict_time(fine_data)
        coarse_space_time_data = self._restrict_space(coarse_time_data)

        assert_condition(self.coarse_level is not None and self.coarse_level.validate_data(coarse_space_time_data),
                         ValueError, message="Restricted Space-Time Data is incompatible to Coarse Level: %s"
                                             % coarse_space_time_data,
                         checking_obj=self)
        return coarse_space_time_data

    @property
    def coarse_level(self):
        # calling weakref to access referenced object
        return self._coarse_level() if self._coarse_level is not None else None

    @coarse_level.setter
    def coarse_level(self, coarse_level):
        assert_is_instance(coarse_level, ReferenceType, descriptor="Reference to Coarse Level", checking_obj=self)
        assert_is_instance(coarse_level(), AbstractLevel, descriptor="Coarse Level", checking_obj=self)
        self._coarse_level = coarse_level

    @property
    def fine_level(self):
        # calling weakref to access referenced object
        return self._fine_level() if self._fine_level is not None else None

    @fine_level.setter
    def fine_level(self, fine_level):
        assert_is_instance(fine_level, ReferenceType, descriptor="Reference to Fine Level", checking_obj=self)
        assert_is_instance(fine_level(), AbstractLevel, descriptor="Fine Level", checking_obj=self)
        self._fine_level = fine_level

    @property
    def time_prolongation_operator(self):
        """Accessor for the time prolongation operator.

        Parameters
        ----------
        time_prolongation_operator :
            New time prolongation operator to be used.

        Returns
        -------
        time_prolongation_operator :
            Current time prolongation operator.
        """
        return self._time_prolongation_operator

    @time_prolongation_operator.setter
    def time_prolongation_operator(self, time_prolongation_operator):
        self._time_prolongation_operator = time_prolongation_operator

    @property
    def spatial_prolongation_operator(self):
        """Accessor for the spatial prolongation operator.

        Parameters
        ----------
        spatial_prolongation_operator :
            New spatial prolongation operator to be used.

        Returns
        -------
        spatial_prolongation_operator :
            Current spatial prolongation operator.
        """
        return self._spatial_prolongation_operator

    @spatial_prolongation_operator.setter
    def spatial_prolongation_operator(self, spatial_prolongation_operator):
        self._spatial_prolongation_operator = spatial_prolongation_operator

    @property
    def time_restriction_operator(self):
        """Accessor for the time restriction operator.

        Parameters
        ----------
        time_restriction_operator :
            New time restriction operator to be used.

        Returns
        -------
        time_restriction_operator :
            Current time restriction operator.
        """
        return self._time_restriction_operator

    @time_restriction_operator.setter
    def time_restriction_operator(self, time_restriction_operator):
        self._time_restriction_operator = time_restriction_operator

    @property
    def spatial_restriction_operator(self):
        """Accessor for the spatial restriction operator.

        Parameters
        ----------
        spatial_restriction_operator :
            New spatial restriction operator to be used.

        Returns
        -------
        spatial_restriction_operator :
            Current spatial restriction operator.
        """
        return self._spatial_restriction_operator

    @spatial_restriction_operator.setter
    def spatial_restriction_operator(self, spatial_restriction_operator):
        self._spatial_restriction_operator = spatial_restriction_operator

    @abstractmethod
    def _prolongate_time(self, coarse_data):
        pass

    @abstractmethod
    def _prolongate_space(self, coarse_data):
        pass

    @abstractmethod
    def _restrict_time(self, fine_data):
        pass

    @abstractmethod
    def _restrict_space(self, fine_data):
        pass

    def lines_for_log(self):
        _lines = OrderedDict()
        _lines['Coarse Level'] = self.coarse_level.lines_for_log() if self.coarse_level is not None else 'na'
        _lines['Fine Level'] = self.fine_level.lines_for_log() if self.fine_level is not None else 'na'
        return _lines

    def __str__(self):
        return "%s<0x%x>(coarse_level=%s, fine_level=%s)" \
            % (class_name(self), id(self),
               self.coarse_level if self.coarse_level is not None else None,
               self.fine_level if self.fine_level is not None else None)

    def __repr__(self):
        return "<%s at 0x%x : coarse_level=%r, fine_level=%r>" \
            % (class_name(self), id(self),
               self.coarse_level if self.coarse_level is not None else None,
               self.fine_level if self.fine_level is not None else None)
