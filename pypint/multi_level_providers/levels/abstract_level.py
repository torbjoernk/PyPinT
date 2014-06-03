# coding=utf-8
"""Abstract Base Class for Levels (space and time).
"""
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from weakref import ReferenceType

from pypint.utilities import assert_is_instance
from pypint.utilities.tracing import class_name


class AbstractLevel(object, metaclass=ABCMeta):
    """Abstract Interface for Levels
    """

    def __init__(self, *args, **kwargs):
        self._ml_provider = None

    @abstractmethod
    def validate_data(self, data):
        """Checks whether given data fits to level

        Parameters
        ----------
        data :
            data to be checked

        Returns
        -------
        data_valid : :py:class:`bool`
            :py:class:`True` if data is valid, :py:class:`False` otherwise
        """
        pass

    @property
    def ml_provider(self):
        """Accessor for the :py:class:`.MultiLevelProvider` this Level is contained in

        Returns
        -------
        ml_provider : :py:class:`.MultiLevelProvider` or :py:class:`None`
            :py:class:`None` is returned if this Level is not stored in a :py:class:`.MultiLevelProvider`

        Raises
        ------
        ValueError :
            If ``value`` is not a :py:class:`weakref.ReferenceType` to a :py:class:`.MultiLevelProvider`.
        """
        if self._ml_provider is None:
            # no weakref to an MultiLevelProvider stored
            return None
        else:
            # calling the weakref object to retreive the MultiLevelProvider
            #  (might return 'None' if the MultiLevelProvider has been destroyed)
            return self._ml_provider()

    @ml_provider.setter
    def ml_provider(self, value):
        assert_is_instance(value, ReferenceType, descriptor="MultiLevelProvider", checking_obj=self)
        self._ml_provider = value

    def lines_for_log(self):
        _lines = OrderedDict()
        return _lines

    def __str__(self):
        _outstr = "%s<0x%x>()" % (class_name(self), id(self))
        return _outstr

    def __repr__(self):
        _repr = "<%s at 0x%x>" % (class_name(self), id(self))
        return _repr


__all__ = ['AbstractLevel']
