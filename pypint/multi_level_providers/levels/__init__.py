# coding=utf-8
"""Providers for Space and Time Levels

.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from enum import Enum, unique


@unique
class LevelHierarchyPosition(Enum):
    undefined = -1
    coarsest = 0
    intermediate = 1
    finest = 2


__all__ = ['LevelHierarchyPosition']
