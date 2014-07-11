# coding=utf-8
import unittest

from pypint.integrators.sdc.abstract_sdc import AbstractSdc


class SdcIntegratorImplementation(AbstractSdc):
    def __init__(self, *args, **kwargs):
        super(SdcIntegratorImplementation, self).__init__(*args, **kwargs)

    def run(self, state, **kwargs):
        super(SdcIntegratorImplementation, self).run(state, **kwargs)

    @property
    def name(self):
        return super(SdcIntegratorImplementation, self.__class__).name.fget(self)


class AbstractSdcTest(unittest.TestCase):
    def setUp(self):
        self.default = SdcIntegratorImplementation()

    def test_has_a_name(self):
        self.assertRegex(self.default.name, '^SDC Integrator Interface$')


if __name__ == '__main__':
    unittest.main()
