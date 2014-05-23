# coding=utf-8
import unittest

from pypint.multi_level_providers.level_providers.abstract_level import AbstractLevel
from pypint.multi_level_providers.level_providers import LevelHierarchyPosition


class AbstractLevelTest(unittest.TestCase):
    def setUp(self):
        self._default = AbstractLevel()

    def test_property_hierarchy_position(self):
        self.assertIsInstance(self._default.hierarchy_position, LevelHierarchyPosition)

        self.assertIs(self._default.hierarchy_position, LevelHierarchyPosition.undefined)

        self._default.hierarchy_position = LevelHierarchyPosition.coarsest
        self.assertIs(self._default.hierarchy_position, LevelHierarchyPosition.coarsest)


if __name__ == '__main__':
    unittest.main()
