# coding=utf-8
import numpy as np

from pypint.problems.i_problem import IProblem
from tests import NumpyAwareTestCase


class IProblemTest(NumpyAwareTestCase):
    def setUp(self):
        self._default = IProblem()

    def test_takes_a_function(self):
        def _test_func():
            return np.array([np.pi]).reshape(self._default.dim)
        _test_obj = IProblem(rhs_function_wrt_time=_test_func)
        self.assertTrue(callable(_test_obj.rhs_function_wrt_time))
        self.assertEqual(_test_obj.rhs_function_wrt_time(), np.pi)

    def test_takes_a_numeric_type(self):
        _test_obj = IProblem(numeric_type=np.float)
        self.assertEqual(_test_obj.numeric_type, np.float)
        _test_obj = IProblem(numeric_type=np.complex)
        self.assertEqual(_test_obj.numeric_type, np.complex)
        self.assertRaises(ValueError, IProblem, numeric_type=bool)
        self.assertRaises(Exception, IProblem, numeric_type="not a type")

    def test_has_a_spacial_dimension(self):
        self.assertEqual(self._default.dim, (1, 1))
        self.assertEqual(self._default.spacial_dim, (1, ))
        self.assertEqual(self._default.dofs_per_point, 1)
        self.assertEqual(self._default.num_spacial_points, 1)

        _test_obj = IProblem(dim=(3, 2, 1))
        self.assertEqual(_test_obj.spacial_dim, (3, 2))
        self.assertEqual(_test_obj.dofs_per_point, 1)
        self.assertEqual(_test_obj.num_spacial_points, 6)

        _test_obj = IProblem(dim=(3, 3, 2))
        self.assertEqual(_test_obj.spacial_dim, (3, 3))
        self.assertEqual(_test_obj.dofs_per_point, 2)
        self.assertEqual(_test_obj.num_spacial_points, 9)

    def test_provides_evaluation(self):
        self._default.evaluate_wrt_time(0.0, np.array([1.0]))
        self.assertRaises(ValueError, self._default.evaluate_wrt_time, complex(1.0, 1.0), np.array([1.0]))
        self.assertRaises(ValueError, self._default.evaluate_wrt_time, 1.0, 1.0)

    def test_provides_implicit_solver(self):
        _test_obj = IProblem(dim=(3, 2, 1))
        _next_x = np.arange(6).reshape(_test_obj.dim_for_time_solver)
        _func = lambda x: np.ones(x.shape)
        _x = _test_obj.implicit_solve(_next_x, _func)
        self.assertNumpyArrayAlmostEqual(_x, _next_x)

        self.assertRaises(ValueError, _test_obj.implicit_solve, 1.0, _func)
        self.assertRaises(ValueError, _test_obj.implicit_solve, _next_x, "not callable")

    def test_takes_descriptive_strings(self):
        self.assertRegex(self._default.__str__(), "IProblem")

        _test_obj = IProblem(strings={'rhs_wrt_time': "Right-Hand Side Formula w.r.t. Time"})
        self.assertRegex(_test_obj.__str__(), "Right-Hand Side Formula")


if __name__ == "__main__":
    import unittest
    unittest.main()
