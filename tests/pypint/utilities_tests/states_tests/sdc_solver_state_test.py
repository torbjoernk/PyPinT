# coding=utf-8
import unittest

from pypint.utilities.states.sdc_solver_state import SdcSolverState
from pypint.utilities.data_structures.scalar_1d import Scalar1D


class SdcSolverStateTest(unittest.TestCase):
    def setUp(self):
        self.default = SdcSolverState(num_nodes=3, type=Scalar1D)
        _ = SdcSolverState(num_time_steps=1, num_nodes=3, type=Scalar1D)

    def test_default(self):
        pass


if __name__ == '__main__':
    unittest.main()
