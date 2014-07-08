# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np

from pypint.utilities.states.state_sequence import StateSequence
from pypint.utilities.assertions import assert_condition


class TimeStepState(StateSequence):
    """Sequence of node states of a single time step.
    """
    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        delta_time_step : :py:class:`float`
            *(optional)*
            Width of the time interval.
            Defaults to 0.0.

        See :py:meth:`.StateSequence.__init__` for further details.
        """
        super(TimeStepState, self).__init__(**kwargs)

        self._delta_time_step = kwargs.get('delta_time_step', 0.0)
        self._initial_node = self._element_type(**kwargs) \
            if not isinstance(kwargs.get('initial'), self._element_type) else kwargs['initial']

    @property
    def delta_time_step(self):
        """Accessor for the width of the time step

        Parameters
        ----------
        delta_time_step : :py:class:`float`

        Returns
        -------
        width_of_time_step : :py:class:`float`

        Raises
        ------
        ValueError
            *(only setter)*
            if ``delta_time_step`` is not a non-zero positive :py:class:`float`
        """
        return self._delta_time_step

    @delta_time_step.setter
    def delta_time_step(self, delta_time_step):
        assert_condition(delta_time_step > 0.0, ValueError,
                         message="Delta interval must be non-zero positive: NOT {}".format(delta_time_step),
                         checking_obj=self)
        self._delta_time_step = delta_time_step

    @property
    def initial_node(self):
        """Accessor for the initial value of this time step
        """
        return self._initial_node

    @initial_node.setter
    def initial_node(self, initial):
        self._initial_node = initial

    @property
    def time_points(self):
        """Read-only accessor for the list of time points of this time step
        """
        return np.array([step.time_point for step in self], dtype=float)

    @property
    def current_time_point(self):
        """Accessor for the current step's time point

        Returns
        -------
        current_time_point : :py:class:`float` or :py:class:`None`
            :py:class:`None` is returned if :py:attr:`.current_node` is :py:class:`None`
        """
        return self.current_node.time_point if self.current_node is not None else None

    @property
    def previous_time_point(self):
        """Accessor for the previous step's time point

        Returns
        -------
        previous_time_point : :py:class:`float` or :py:class:`None`
            :py:class:`None` is returned if :py:attr:`.previous_node` is :py:class:`None`
        """
        return self.previous_node.time_point if self.previous_node is not None else None

    @property
    def next_time_point(self):
        """Accessor for the next step's time point

        Returns
        -------
        next_time_point : :py:class:`float` or :py:class:`None`
            :py:class:`None` is returned if :py:attr:`.next_node` is :py:class:`None`
        """
        return self.next.time_point if self.next_node is not None else None

    @property
    def current_node(self):
        """Proxy for :py:attr:`.current`
        """
        return self.current

    @property
    def current_node_index(self):
        """Proxy for :py:attr:`.current_index`
        """
        return self.current_index

    @property
    def previous_node(self):
        """Accessor for the previous step

        Returns
        -------
        previous step : :py:class:`.NodeState` or :py:class:`None`
            :py:class:`None` is returned if :py:attr:`.previous_index` is :py:class:`None`
        """
        return self.previous if self.previous_index is not None else self.initial_node

    @property
    def previous_node_index(self):
        """Proxy for :py:attr:`.previous_index`
        """
        return self.previous_index

    @property
    def next_node(self):
        """Proxy for :py:attr:`.next`
        """
        return self.next

    @property
    def next_node_index(self):
        """Proxy for :py:attr:`.next_index`
        """
        return self.next_index

    @property
    def last_node(self):
        """Proxy for :py:attr:`.last`
        """
        return self.last

    @property
    def last_node_index(self):
        """Proxy for :py:attr:`.last_index`
        """
        return self.last_index


__all__ = ['TimeStepState']
