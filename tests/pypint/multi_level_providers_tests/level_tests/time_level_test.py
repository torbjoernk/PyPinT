# coding=utf-8
import unittest
from unittest.mock import MagicMock
import warnings

from pypint.multi_level_providers.levels.time_level import TimeLevel
from pypint.multi_level_providers.levels.abstract_level import AbstractLevel
from pypint.integrators.abstract_integrator import AbstractIntegrator
from pypint.utilities.quadrature.nodes.abstract_nodes import AbstractNodes


class TimeLevelTest(unittest.TestCase):
    def setUp(self):
        self._default = TimeLevel()
        self._integrator = MagicMock(AbstractIntegrator, name="AbstractIntegrator",
                                     nodes=MagicMock(AbstractNodes, name="Nodes"),
                                     num_nodes=3)

    def test_is_an_abstract_level(self):
        # this does imply, that TimeLevel has the same behaviour as an AbstractLevel; but is a strong indicator that
        #  it does so
        self.assertIsInstance(self._default, AbstractLevel)

    def test_has_integrator_accessor(self):
        self.assertIsNone(self._default.integrator, "no default Integrator set")

        _test_obj = TimeLevel(integrator=self._integrator)
        self.assertIs(_test_obj.integrator, self._integrator)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertIsNone(self._default.nodes)
            self.assertEqual(len(w), 1,
                             "Property `nodes` should raise a warning on absence of Integrator")
            self.assertTrue(issubclass(w[-1].category, UserWarning))

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertIsNone(self._default.num_nodes)
            self.assertEqual(len(w), 1,
                             "Property `num_nodes` should raise a warning on absence of Integrator")
            self.assertTrue(issubclass(w[-1].category, UserWarning))

        self._default.integrator = self._integrator
        self.assertIs(self._default.integrator, self._integrator)
        self.assertIsNotNone(self._default.nodes)
        self.assertIs(self._default.nodes, self._integrator.nodes)
        self.assertIsNotNone(self._default.num_nodes)
        self.assertIs(self._default.num_nodes, self._integrator.num_nodes)

    def test_can_validate_data(self):
        _valid_data = [1, 2, 3]
        _invalid_data1 = [1, 2]
        _invalid_data2 = 'not a list'

        self._default.integrator = self._integrator

        self.assertTrue(self._default.validate_data(_valid_data))

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.assertFalse(self._default.validate_data(_invalid_data1))
            self.assertGreaterEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.assertFalse(self._default.validate_data(_invalid_data2))
            self.assertGreaterEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

    def test_provides_stringification(self):
        self.assertIsNotNone(self._default.lines_for_log())
        self.assertIn('Integrator', self._default.lines_for_log().keys())

        self.assertRegex(str(self._default), '^TimeLevel<0x[0-9a-f]*>\(integrator=.*\)$')

        self.assertRegex(repr(self._default), '^<TimeLevel at 0x[0-9a-f]* : integrator=.*>$')


if __name__ == '__main__':
    unittest.main()
