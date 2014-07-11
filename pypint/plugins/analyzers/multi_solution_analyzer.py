# coding=utf-8
"""

.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np

from pypint.plugins.analyzers.i_analyzer import IAnalyzer
from pypint.plugins.plotters.reduction_residual_plotter import ReductionResidualPlotter
from pypint.solvers.i_iterative_time_solver import IIterativeTimeSolver
from pypint.utilities.states.solver_state import SolverState
from pypint.utilities import assert_named_argument


class MultiSolutionAnalyzer(IAnalyzer):
    """Analyzer for multiple solver states

    For now, it only plots the final residual vs. final reduction of all given states.
    Only up to seven separate states are supported.
    """
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        plotter_options : :py:class:`dict`
            options to be passed on to the plotter
        """
        super(MultiSolutionAnalyzer, self).__init__(args, **kwargs)

        if 'plotter_options' in kwargs:
            self._plotter = ReductionResidualPlotter(**kwargs['plotter_options'])
        else:
            self._plotter = ReductionResidualPlotter()

        self._solvers = []
        self._data = []

    def run(self, **kwargs):
        """Executes the analysis
        """
        super(MultiSolutionAnalyzer, self).run(**kwargs)

        # plot the last solution
        self._plotter.plot(solvers=np.array(self._solvers),
                           states=np.array(self._data))

    def add_data(self, *args, **kwargs):
        """
        Parameters
        ----------
        solver : :py:class:`.IIterativeTimeSolver`
            solver

        state : :py:class:`.SolverState`
            state of the solver

        Raises
        ------
        ValueError

            * if ``solver`` is not given or is not a :py:class:`.IIterativeTimeSolver`
            * if ``state`` is not given or is not a :py:class:`.SolverState`
        """
        super(MultiSolutionAnalyzer, self).add_data(args, kwargs)

        assert_named_argument('solver', kwargs, types=IIterativeTimeSolver,
                              descriptor="Solver", checking_obj=self)

        assert_named_argument('state', kwargs, types=SolverState, descriptor="State", checking_obj=self)

        self._solvers.append(kwargs['solver'])
        self._data.append(kwargs['state'])
