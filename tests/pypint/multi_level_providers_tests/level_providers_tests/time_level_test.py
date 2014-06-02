# coding=utf-8
import unittest
from unittest.mock import MagicMock, PropertyMock
import warnings

from pypint.multi_level_providers.level_providers.time_level import TimeLevel
from pypint.multi_level_providers.level_providers.abstract_level import AbstractLevel
from pypint.integrators.i_integrator import IIntegrator
from pypint.utilities.quadrature.node_providers.i_nodes import INodes


class TimeLevelTest(unittest.TestCase):
    def setUp(self):
        self._default = TimeLevel()
        self._integrator = MagicMock(IIntegrator, name="IIntegrator")
        self._nodes = PropertyMock(return_value=MagicMock(INodes, name="Nodes"))
        self._integrator.nodes = self._nodes
        self._num_nodes = PropertyMock(return_value=3)
        self._integrator.num_nodes = self._num_nodes

    def test_is_an_abstract_level(self):
        self.assertIsInstance(self._default, AbstractLevel)

    def test_has_integrator_accessor(self):
        self.assertIsNone(self._default.integrator, "no default Integrator set")

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

    def test_provides_stringification(self):
        self.assertIsNotNone(self._default.lines_for_log())
        self.assertIn('Integrator', self._default.lines_for_log().keys())

        self.assertRegex(str(self._default), '^TimeLevel<0x[0-9a-f]*>\(integrator=.*\)$')

        self.assertRegex(repr(self._default), '^<TimeLevel at 0x[0-9a-f]* : integrator=.*>$')


if __name__ == '__main__':
    unittest.main()
