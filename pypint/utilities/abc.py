# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from abc import ABCMeta, abstractmethod
from collections.abc import Hashable
from copy import deepcopy


class Comparable(Hashable, metaclass=ABCMeta):

    __slots__ = ()

    @abstractmethod
    def __eq__(self, other):
        if not isinstance(other, Comparable):
            return NotImplemented
        return False

    @abstractmethod
    def __lt__(self, other):
        if not isinstance(other, Comparable):
            return NotImplemented
        return False

    def __le__(self, other):
        if not isinstance(other, Comparable):
            return NotImplemented
        if self == other:
            return True
        elif self < other:
            return True
        else:
            return False

    def __gt__(self, other):
        if not isinstance(other, Comparable):
            return NotImplemented
        return not self <= other

    def __ge__(self, other):
        if not isinstance(other, Comparable):
            return NotImplemented
        return not self < other

    def __ne__(self, other):
        return not (self == other)

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Comparable:
            if any('__eq__' in B.__dict__ for B in C.__mro__)\
                    and any('__le__' in B.__mro__ for B in C.__mro__)\
                    and any('__lt__' in B.__dict__ for B in C.__mro__)\
                    and any('__gt__' in B.__mro__ for B in C.__mro__)\
                    and any('__ge__' in B.__mro__ for B in C.__mro__)\
                    and any('__ne__' in B.__mro__ for B in C.__mro__):
                return True
        return NotImplemented


class Copyable(metaclass=ABCMeta):

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
