# coding=utf-8
import unittest


from pypint.integrators.abstract_integrator import AbstractIntegrator


class IntegratorImplementation(AbstractIntegrator):
    def __init__(self, *args, **kwargs):
        super(IntegratorImplementation, self).__init__(*args, **kwargs)

    def run(self, state, **kwargs):
        super(IntegratorImplementation, self).run(state, **kwargs)

    def compute_residual(self, state, **kwargs):
        super(IntegratorImplementation, self).compute_residual(state, **kwargs)

    def compute_error(self, state, **kwargs):
        super(IntegratorImplementation, self).compute_error(state, **kwargs)

    @property
    def name(self):
        return super(self.__class__, self.__class__).name.fget(self)


class AbstractIntegratorTest(unittest.TestCase):
    def setUp(self):
        self.default = IntegratorImplementation()

    def test_has_a_name(self):
        self.assertRegex(self.default.name, '^Integrator Interface$')


if __name__ == '__main__':
    unittest.main()
