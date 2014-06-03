# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from numpy import dtype as np_dtype

from pypint.utilities.abc import Comparable, Deepcopyable
from pypint.utilities import assert_is_instance, class_name


class AbstractSpatialObject(Comparable, Deepcopyable, metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self._dtype = None
        if 'dtype' in kwargs:
            self.dtype = kwargs['dtype']

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        assert_is_instance(dtype, np_dtype, descriptor="Numerics Type", checking_obj=self)
        self._dtype = dtype

    @abstractmethod
    def set(self, *args, **kwargs):
        return NotImplemented

    @abstractmethod
    @property
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

    @abstractmethod
    def __imul__(self, other):
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
