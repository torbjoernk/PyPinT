# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from abc import ABCMeta
from copy import deepcopy


class Copyable(metaclass=ABCMeta):
    """Abstract Base Class providing shallow coppies of derived types
    """

    __slots__ = ()

    def __copy__(self):
        _copy = self.__class__.__new__(self.__class__)
        _copy.__dict__.update(self.__dict__)
        return _copy

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Copyable:
            if any('__copy__' in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


class Deepcopyable(Copyable, metaclass=ABCMeta):
    """Abstract Base Class providing shallow and deep coppies of derived types
    """

    __slots__ = ()

    def __deepcopy__(self, memo):
        _copy = self.__class__.__new__(self.__class__)
        memo[id(self)] = _copy
        for item, value in self.__dict__.items():
            setattr(_copy, item, deepcopy(value, memo))
        return _copy

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Deepcopyable:
            if any('__deepcopy__' in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


__all__ = ['Comparable', 'Copyable', 'Deepcopyable']
