# coding=utf-8
import unittest
from unittest.mock import MagicMock, patch
import weakref

import numpy
from nose.tools import *

from pypint.multi_level_providers.transitioners.space_invariant_time_transitioner import SpaceInvariantTimeTransitioner
from pypint.multi_level_providers.transitioners.abstract_transitioner import AbstractTransitioner
from pypint.multi_level_providers.levels.time_level import TimeLevel
from tests import assert_numpy_array_almost_equal


test_data = [
    {
        'coarse_level': MagicMock(TimeLevel, 'Coarse TimeLevel', num_nodes=3, nodes=numpy.linspace(0.0, 1.0, 3)),
        'fine_level': MagicMock(TimeLevel, 'Coarse TimeLevel', num_nodes=5, nodes=numpy.linspace(0.0, 1.0, 5)),
        'coarse_data': numpy.ones(3),
        'fine_data': numpy.ones(5)
    }
]


def prolongate(data_set):
    _test_obj = SpaceInvariantTimeTransitioner(coarse_level=weakref.ref(data_set['coarse_level']),
                                               fine_level=weakref.ref(data_set['fine_level']))
    prolongated = _test_obj.prolongate(data_set['coarse_data'])
    assert_equal(len(prolongated), data_set['fine_data'].size)
    assert_numpy_array_almost_equal(data_set['fine_data'], numpy.asarray(prolongated))


def restrict(data_set):
    _test_obj = SpaceInvariantTimeTransitioner(coarse_level=weakref.ref(data_set['coarse_level']),
                                               fine_level=weakref.ref(data_set['fine_level']))
    restricted = _test_obj.restrict(data_set['fine_data'])
    assert_equal(len(restricted), data_set['coarse_data'].size)
    assert_numpy_array_almost_equal(data_set['coarse_data'], numpy.asarray(restricted))


def test_prolongation():
    for data_set in test_data:
        yield prolongate, data_set


def test_restriction():
    for data_set in test_data:
        yield restrict, data_set


class SpaceInvariantTimeTransitionerTest(unittest.TestCase):
    def setUp(self):
        self._default = SpaceInvariantTimeTransitioner()

        self._lagrage_patch = patch('pypint.multi_level_providers.transitioners.space_invariant_time_transitioner'
                                    '.lagrange_polynome',
                                    lambda *args: 1.0)
        self._lagrage_patch.start()

        self._coarse_level = MagicMock(TimeLevel, name='Coarse TimeLevel',
                                       num_nodes=3,
                                       nodes=numpy.array([-1.0, 0.0, 1.0]),
                                       lines_for_log=lambda: 'an OrderedDict')
        self._fine_level = MagicMock(TimeLevel, name='Fine TimeLevel',
                                     num_nodes=5,
                                     nodes=numpy.array([-1.0, -0.5, 0.0, 0.5, 1.0]),
                                     lines_for_log=lambda: 'an OrderedDict')

    def tearDown(self):
        self._lagrage_patch.stop()

    def test_is_abstract_level_transitioner(self):
        # this does imply, that SpaceInvariantTimeTransitioner has the same behaviour as an AbstractTransitioner;
        #  but is a strong indicator that it does so
        self.assertIsInstance(self._default, AbstractTransitioner)

    def test_has_coarse_level_accessor(self):
        self.assertIsNone(self._default.coarse_level, "Defaults to None")

        self._default.coarse_level = weakref.ref(self._coarse_level)
        self.assertIs(self._default.coarse_level, self._coarse_level)

        with self.assertRaises(ValueError, msg="Requires weakref to Level not Level itself"):
            self._default.coarse_level = self._coarse_level

    def test_has_fine_level_accessor(self):
        self.assertIsNone(self._default.fine_level, "Defaults to None")

        self._default.fine_level = weakref.ref(self._fine_level)
        self.assertIs(self._default.fine_level, self._fine_level)

        with self.assertRaises(ValueError, msg="Requires weakref to Level not Level itself"):
            self._default.fine_level = self._fine_level

    def test_auto_computes_time_restriction_and_prolongation_operators(self):
        self.assertIsNone(self._default.time_restriction_operator)
        self.assertIsNone(self._default.time_prolongation_operator)

        self._default.coarse_level = weakref.ref(self._coarse_level)
        self._default.fine_level = weakref.ref(self._fine_level)

        self.assertIsNotNone(self._default.time_restriction_operator)
        self.assertTrue(all(elem == 1.0 for elem in self._default.time_restriction_operator.flatten()))
        self.assertIsNotNone(self._default.time_prolongation_operator)
        self.assertTrue(all(elem == 1.0 for elem in self._default.time_prolongation_operator.flatten()))

    def test_provides_stringification(self):
        self.assertIsNotNone(self._default.lines_for_log())
        self.assertRegex(str(self._default),
                         '^SpaceInvariantTimeTransitioner<0x[0-9a-f]*>\(coarse_level=None, fine_level=None\)$')

        self.assertRegex(repr(self._default),
                         '^<SpaceInvariantTimeTransitioner at 0x[0-9a-f]* : coarse_level=None, fine_level=None>$')
        self.assertIn('Coarse Level', self._default.lines_for_log())
        self.assertIs(self._default.lines_for_log()['Coarse Level'], 'na')
        self.assertIn('Fine Level', self._default.lines_for_log())
        self.assertIs(self._default.lines_for_log()['Fine Level'], 'na')

        self._default.coarse_level = weakref.ref(self._coarse_level)
        self._default.fine_level = weakref.ref(self._fine_level)
        self.assertRegex(str(self._default),
                         '^SpaceInvariantTimeTransitioner<0x[0-9a-f]*>\(coarse_level=.*, fine_level=.*\)$')

        self.assertRegex(repr(self._default),
                         '^<SpaceInvariantTimeTransitioner at 0x[0-9a-f]* : coarse_level=.*, fine_level=.*>$')
        self.assertIn('Coarse Level', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Coarse Level'], 'an OrderedDict')
        self.assertIn('Fine Level', self._default.lines_for_log())
        self.assertEqual(self._default.lines_for_log()['Fine Level'], 'an OrderedDict')


if __name__ == '__main__':
    unittest.main()
