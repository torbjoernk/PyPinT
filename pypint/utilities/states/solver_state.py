# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.kaltt@fz-juelich.de>
"""
from pypint.utilities.states.state_sequence import StateSequence
from pypint.solutions.final_solution import FinalSolution
from pypint.solutions.iterative_solution import IterativeSolution
from pypint.solutions.data_storage.trajectory_solution_data import TrajectorySolutionData
from pypint.utilities.assertions import assert_condition


class SolverState(StateSequence):
    """Stores iteration states.
    """
    def __init__(self, **kwargs):
        if 'solution_type' not in kwargs:
            kwargs['solution_type'] = [FinalSolution, IterativeSolution, TrajectorySolutionData]
        super(SolverState, self).__init__(**kwargs)

        self._delta_interval = kwargs.get('delta_interval', 0.0)

    @property
    def delta_interval(self):
        """Accessor for the total interval width.

        Parameters
        ----------
        delta_interval : :py:class:`float`
            width of the whole interval

        Raises
        ------
        ValueError
            if given interval is not a non-zero float
        """
        return self._delta_interval

    @delta_interval.setter
    def delta_interval(self, delta_interval):
        assert_condition(delta_interval > 0.0, ValueError,
                         message="Delta interval must be non-zero positive: NOT {}".format(delta_interval),
                         checking_obj=self)
        self._delta_interval = delta_interval

    @property
    def current_iteration(self):
        """Proxies :py:attr:`.MutableStateSequence.current`
        """
        return self.current

    @property
    def current_iteration_index(self):
        """Proxies :py:attr:`.MutableStateSequence.current_index`
        """
        return self.current_index

    @property
    def previous_iteration(self):
        """Proxies :py:attr:`.MutableStateSequence.previous`
        """
        return self.previous

    @property
    def previous_iteration_index(self):
        """Proxies :py:attr:`.MutableStateSequence.previous_index`
        """
        return self.previous_index

    @property
    def first_iteration(self):
        """Proxies :py:attr:`.MutableStateSequence.first`
        """
        return self.first

    @property
    def is_first_iteration(self):
        """Check on whether current iteration is the first one.

        Returns
        -------
        is_first : :py:class:`bool`
            :py:class:`True` if ``len(self)`` is one, :py:class:`False` otherwise
        """
        return self.current_iteration_index == 0

    @property
    def last_iteration(self):
        """Proxies :py:attr:`.MutableStateSequence.last`
        """
        return self.last

    @property
    def last_iteration_index(self):
        """Proxies :py:attr:`.MutableStateSequence.last_index`
        """
        return self.last_index


__all__ = ['SolverState']
