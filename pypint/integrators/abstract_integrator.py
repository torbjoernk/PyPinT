# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from abc import ABCMeta, abstractmethod

from pypint.utilities import assert_is_instance
from pypint.utilities.states.solver_state import SolverState


class AbstractIntegrator(metaclass=ABCMeta):
    """Interface for the Solver's Cores
    """

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, state, **kwargs):
        """Apply the solver core to the current state

        Parameters
        ----------
        state : :py:class:`.SolverState`
            Current state of the solver.
        """
        assert_is_instance(state, SolverState, descriptor="Solver's State", checking_obj=self)

    @abstractmethod
    def compute_residual(self, state, **kwargs):
        """Computes the residual of the current state

        Parameters
        ----------
        state : :py:class:`.SolverState`
            Current state of the solver.
        """
        assert_is_instance(state, SolverState, descriptor="Solver's State", checking_obj=self)

    @abstractmethod
    def compute_error(self, state, **kwargs):
        """Computes the error of the current state

        Parameters
        ----------
        state : :py:class:`.SolverState`
            Current state of the solver.
        """
        assert_is_instance(state, SolverState, descriptor="Solver's State", checking_obj=self)

    @property
    @abstractmethod
    def name(self):
        """Human readable name of the solver's core
        """
        return 'Solver Core Interface'


__all__ = ['AbstractIntegrator']
