# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

import numpy as np

from pypint.utilities.abc import Deepcopyable
from pypint.utilities import assert_is_instance, class_name


class AbstractSpatialObject(Deepcopyable, metaclass=ABCMeta):
    """Abstract Base Class for spatial objects

    Implementations must override the following methods:

    :py:meth:`.set`:
        setter for the contained data values
    :py:attr:`.norm`:
        defining a useful norm of the contained data values
    :py:meth:`.__add__`:
        for simple addition of scalars and other spatial objects
    :py:meth:`.__iadd__`:
        for simple in-place addition of scalars and other spatial objects
    :py:meth:`.__sub__`:
        for simple subtraction of scalars and other spatial objects
    :py:meth:`.__isub__`:
        for simple in-place subtraction of scalars and other spatial objects
    :py:meth:`.__mul__`:
        for simple multiplication (``3 * my_spatial_object``)
    :py:meth:`.__imul__`:
        for in-place multiplication (``my_spatial_object *= 3``)
    :py:meth:`.__neg__`:
        to provide operations as ``-my_spatial_object``
    :py:meth:`.__pos__`:
        to provide operations as ``+my_spatial_object``
    """

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        dtype : :py:class:`numpy.dtype`
            numerical type of the contained data
        """
        self._dtype = None
        if 'dtype' in kwargs:
            self.dtype = kwargs['dtype']

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        if not isinstance(dtype, np.dtype):
            dtype = np.dtype(dtype)
        assert_is_instance(dtype, np.dtype, descriptor="Numerics Type", checking_obj=self)
        self._dtype = dtype

    @abstractmethod
    def set(self, *args, **kwargs):
        return NotImplemented

    @property
    @abstractmethod
    def norm(self):
        return NotImplemented

    @abstractmethod
    def __add__(self, other):
        return NotImplemented

    @abstractmethod
    def __iadd__(self, other):
        return NotImplemented

    @abstractmethod
    def __sub__(self, other):
        return NotImplemented

    @abstractmethod
    def __isub__(self, other):
        return NotImplemented

    @abstractmethod
    def __mul__(self, other):
        return NotImplemented

    @abstractmethod
    def __imul__(self, other):
        return NotImplemented

    @abstractmethod
    def __neg__(self):
        return NotImplemented

    @abstractmethod
    def __pos__(self):
        return NotImplemented

    def lines_for_log(self):
        _lines = OrderedDict()
        _lines['Numeric Type'] = "%s" % self.dtype
        return _lines

    def __str__(self):
        return "%s<0x%x>(dtype=%s)" % (class_name(self), id(self), self.dtype)

    def __repr__(self):
        return "<%s at 0x%x : dtype=%r>" % (class_name(self), id(self), self.dtype)


__all__ = ['AbstractSpatialObject']
