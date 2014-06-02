# coding=utf-8
import unittest
from unittest.mock import MagicMock
import weakref

from pypint.multi_level_providers.level_providers.abstract_level import AbstractLevel
from pypint.multi_level_providers.multi_level_provider import MultiLevelProvider


class AbstractLevelTest(unittest.TestCase):
    def setUp(self):
        self._default = AbstractLevel()

        self._ml_provider = MagicMock(MultiLevelProvider, name="MultiLevelProvider")

    def test_has_ml_provider_accessor(self):
        self.assertIsNone(self._default.ml_provider, "no MultiLevelProvider given by default")

        self._default.ml_provider = weakref.ref(self._ml_provider)
        self.assertIs(self._default.ml_provider, self._ml_provider)

        with self.assertRaises(ValueError):
            self._default.ml_provider = self._ml_provider

    def test_provides_stringification(self):
        self.assertIsNotNone(self._default.lines_for_log())

        self.assertRegex(str(self._default), '^AbstractLevel<0x[0-9a-f]*>\(\)$')

        self.assertRegex(repr(self._default), '^<AbstractLevel at 0x[0-9a-f]*>$')


if __name__ == '__main__':
    unittest.main()
