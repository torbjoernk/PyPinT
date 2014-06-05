# coding=utf-8
import unittest
from unittest.mock import MagicMock, ANY

from pypint.multi_level_providers.multi_level_provider import MultiLevelProvider
from pypint.multi_level_providers.levels.abstract_level import AbstractLevel
from pypint.multi_level_providers.transitioners.abstract_transitioner import AbstractTransitioner


class MultiLevelProviderTest(unittest.TestCase):
    def setUp(self):
        self._coarsest_level = MagicMock(AbstractLevel, 'Coarsest Level')
        self._intermediate_level = MagicMock(AbstractLevel, 'Intermediate Level')
        self._finest_level = MagicMock(AbstractLevel, 'Finest Level')

        self._coarse_intermediate = MagicMock(AbstractTransitioner, 'Coarse to Intermediate Transitioner',
                                              coarse_level=self._coarsest_level,
                                              fine_level=self._intermediate_level,
                                              prolongate=lambda *args: 'prolongated data',
                                              restrict=lambda *args: 'restricted data')
        self._intermediate_fine = MagicMock(AbstractTransitioner, 'Intermediate to Fine Transitioner',
                                            coarse_level=self._intermediate_level,
                                            fine_level=self._finest_level,
                                            prolongate=lambda *args: 'prolongated data',
                                            restrict=lambda *args: 'restricted data')

        self._default = MultiLevelProvider()

    def test_is_container_for_levels(self):
        self.assertEqual(self._default.num_levels, 0)
        self._default.add_coarser_level(self._coarsest_level)
        self.assertIn(self._coarsest_level, self._default)
        self.assertNotIn(self._finest_level, self._default)
        self.assertNotIn('not a level', self._default)

    def test_add_and_access_coarser_level(self):
        self.assertEqual(self._default.num_levels, 0)
        self.assertListEqual(self._default.levels, [])

        with self.assertRaises(ValueError):
            self._default.add_coarser_level('not an AbstractLevel')

        self._default.add_coarser_level(self._intermediate_level)
        self.assertEqual(self._default.num_levels, 1)
        self.assertListEqual(self._default.levels, [self._intermediate_level])
        self.assertEqual(self._default.coarsest_level, self._default.finest_level)

        self._default.add_coarser_level(self._coarsest_level)
        self.assertEqual(self._default.num_levels, 2)
        self.assertListEqual(self._default.levels, [self._coarsest_level, self._intermediate_level])

        self.assertEqual(self._default.level(0), self._coarsest_level)
        self.assertEqual(self._default.level(1), self._intermediate_level)
        with self.assertRaises(IndexError):
            self._default.level(2)

    def test_add_and_access_finer_level(self):
        self.assertEqual(self._default.num_levels, 0)
        self.assertListEqual(self._default.levels, [])

        with self.assertRaises(ValueError):
            self._default.add_finer_level('not an AbstractLevel')

        self._default.add_finer_level(self._intermediate_level)
        self.assertEqual(self._default.num_levels, 1)
        self.assertListEqual(self._default.levels, [self._intermediate_level])
        self.assertEqual(self._default.coarsest_level, self._default.finest_level)

        self._default.add_finer_level(self._finest_level)
        self.assertEqual(self._default.num_levels, 2)
        self.assertListEqual(self._default.levels, [self._intermediate_level, self._finest_level])

        self.assertEqual(self._default.level(0), self._intermediate_level)
        self.assertEqual(self._default.level(1), self._finest_level)
        with self.assertRaises(IndexError):
            self._default.level(2)

    def test_relative_level_accessors(self):
        self._default.add_coarser_level(self._coarsest_level)
        self._default.add_finer_level(self._finest_level)
        self.assertEqual(self._default.num_levels, 2)

        self.assertEqual(self._default.get_coarser_level(self._finest_level), self._coarsest_level)
        self.assertIsNone(self._default.get_coarser_level(self._coarsest_level))

        self.assertEqual(self._default.get_finer_level(self._coarsest_level), self._finest_level)
        self.assertIsNone(self._default.get_finer_level(self._finest_level))

        with self.assertRaises(ValueError):
            self._default.get_finer_level(self._intermediate_level)

        with self.assertRaises(ValueError):
            self._default.get_coarser_level(self._intermediate_level)

    def test_add_transitioners(self):
        self._default.add_coarser_level(self._coarsest_level)
        self._default.add_finer_level(self._intermediate_level)
        self.assertEqual(self._default.num_levels, 2)

        self._default.add_level_transition(self._coarse_intermediate)

        with self.assertRaises(ValueError):
            self._default.add_level_transition(self._intermediate_fine)

        self._default.add_finer_level(self._finest_level)
        self.assertEqual(self._default.num_levels, 3)
        with self.assertRaises(RuntimeError):
            self._default.restrict(ANY, self._finest_level, self._intermediate_level)
        self._default.add_level_transition(self._intermediate_fine)

    def test_restriction_and_prolongation(self):
        self._default.add_coarser_level(self._coarsest_level)
        self._default.add_finer_level(self._intermediate_level)
        self.assertEqual(self._default.num_levels, 2)
        self._default.add_level_transition(self._coarse_intermediate)

        self.assertEqual(self._default.restrict(ANY, self._intermediate_level, self._coarsest_level),
                         'restricted data')
        self.assertEqual(self._default.restrict(ANY, self._intermediate_level), 'restricted data')
        self.assertEqual(self._default.prolongate(ANY, self._coarsest_level, self._intermediate_level),
                         'prolongated data')
        self.assertEqual(self._default.prolongate(ANY, self._coarsest_level), 'prolongated data')

    def test_provides_stringification(self):
        self.assertRegex(str(self._default), '^MultiLevelProvider<0x[0-9a-f]*>\(num_level=0\)$')
        self.assertRegex(repr(self._default), '^<MultiLevelProvider at 0x[0-9a-f]* : num_level=0>$')
        self.assertIn('Number Levels', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Number Levels'], '0')
        self.assertIn('Levels', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Levels'], 'na')
        self.assertIn('Transitioners', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Transitioners'], 'na')

        self._default.add_coarser_level(self._coarsest_level)
        self._default.add_finer_level(self._intermediate_level)
        self.assertEqual(self._default.num_levels, 2)
        self._default.add_level_transition(self._coarse_intermediate)
        self.assertRegex(str(self._default), '^MultiLevelProvider<0x[0-9a-f]*>\(num_level=2\)$')
        self.assertRegex(repr(self._default), '^<MultiLevelProvider at 0x[0-9a-f]* : num_level=2>$')
        self.assertIn('Number Levels', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Number Levels'], '2')
        self.assertIn('Levels', self._default.lines_for_log())
        self.assertIn('Coarsest', self._default.lines_for_log()['Levels'])
        self.assertIn('Finest', self._default.lines_for_log()['Levels'])
        self.assertIn('Transitioners', self._default.lines_for_log())

        self._default.add_finer_level(self._finest_level)
        self.assertEqual(self._default.num_levels, 3)
        self._default.add_level_transition(self._intermediate_fine)
        self.assertEqual(self._default.lines_for_log()['Number Levels'], '3')
        self.assertIn('Intermediate', self._default.lines_for_log()['Levels'])


if __name__ == "__main__":
    unittest.main()
