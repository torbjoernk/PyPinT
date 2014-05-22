# coding=utf-8
"""Abstract Base Class for Levels (space and time).
"""
from abc import ABCMeta
from collections import OrderedDict

from pypint.multi_level_providers.level_providers import LevelHierarchyPosition
from pypint.utilities import assert_is_instance
from pypint.utilities.tracing import class_name


class AbstractLevel(object, metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        super(AbstractLevel, self).__init__()

        self._hierarchy_position = LevelHierarchyPosition.undefined

    @property
    def hierarchy_position(self):
        return self._hierarchy_position

    @hierarchy_position.setter
    def hierarchy_position(self, value):
        assert_is_instance(value, LevelHierarchyPosition, descriptor="Level's Hierarchy Position", checking_obj=self)
        self._hierarchy_position = value

    def lines_for_log(self):
        _lines = OrderedDict()
        _lines['Hierarchy Position'] = "%s: %d" % (self.hierarchy_position.name, self.hierarchy_position)
        return _lines

    def __str__(self):
        _outstr = "%s<0x%x>(hierarchy_position=%s)" % (class_name(self), id(self), self.hierarchy_position.name)
        return _outstr

    def __repr__(self):
        _repr = "<%s at 0x%x : hierarchy_position=%r>" % (class_name(self), id(self), self.hierarchy_position)
        return _repr


__all__ = ['AbstractLevel']
