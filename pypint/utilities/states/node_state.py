# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from collections import OrderedDict
from weakref import ReferenceType

from pypint.utilities.abc import Deepcopyable
from pypint.solutions.data_storage.step_solution_data import StepSolutionData
from pypint.utilities.data_structures.abstract_spatial_object import AbstractSpatialObject
from pypint.utilities.tracing import class_name
from pypint.utilities.assertions import assert_condition, assert_is_instance, assert_named_argument


class NodeState(Deepcopyable):
    """State of a single node

    A node is a single point in time.

    Parameters
    ----------
    type : :py:class:`type`
        The type of the data values.
        Must be a subclass of :py:class:`.AbstractSpatialObject`.

    Raises
    ------
    ValueError
        If ``type`` is not a :py:class:`type` and not a subclass of :py:class:`.AbstractSpatialObject`.
    """
    def __init__(self, **kwargs):
        assert_named_argument('type', kwargs, types=type, descriptor="Step Data Type", checking_obj=self)
        assert_condition(issubclass(kwargs['type'], AbstractSpatialObject), ValueError,
                         message="Step Data Type must be a Spatial Object: NOT %s" % kwargs['type'],
                         checking_obj=self)
        self._parent = None
        self._data = kwargs['type']()
        self._solution = StepSolutionData()
        self._delta_tau = 0.0
        self._rhs = kwargs['type']()
        self._integral = kwargs['type']()

    def finalize(self):
        """Finalize this state

        This finally stores the :py:attr:`.value` in the solution object and finalizes the :py:attr:`.solution`.
        """
        self.solution.value = self._data
        self.solution.finalize()

    @property
    def parent(self):
        return self._parent() if self._parent else None

    @parent.setter
    def parent(self, value):
        assert_is_instance(value, ReferenceType, descriptor="Parent Container", checking_obj=self)
        self._parent = value

    @property
    def solution(self):
        """Proxy to the included solution of the state

        Returns
        -------
        solution : :py:class:`.StepSolutionData`
        """
        return self._solution

    @property
    def value(self):
        """Proxy for the solution value

        On setting, the right hand side evaluation (:py:attr:`.rhs`) gets reset.
        """
        return self._data

    @value.setter
    def value(self, value):
        assert_is_instance(value, AbstractSpatialObject, descriptor="Data Value", checking_obj=self)
        self._data = value

    @property
    def time_point(self):
        """Proxy for :py:attr:`.StepSolutionData.time_point`
        """
        return self._solution.time_point

    @property
    def rhs(self):
        """Accessor for an evaluation of the Right Hand Side

        Parameters
        ----------
        rhs : :py:class:`.AbstractSpatialObject`

        Raises
        ------
        ValueError
            If value is not a :py:class:`.AbstractSpatialObject` on setting.
        """
        return self._rhs

    @rhs.setter
    def rhs(self, rhs):
        assert_is_instance(rhs, AbstractSpatialObject, descriptor="Right Hand Side Value", checking_obj=self)
        self._rhs = rhs

    @property
    def integral(self):
        """Accessor for an integral value

        Parameters
        ----------
        integral : :py:class:`.AbstractSpatialObject`

        Raises
        ------
        ValueError
            If value is not a :py:class:`.AbstractSpatialObject` on setting.
        """
        return self._integral

    @integral.setter
    def integral(self, integral):
        assert_is_instance(integral, AbstractSpatialObject, descriptor="Integral Value", checking_obj=self)
        self._integral = integral

    @property
    def delta_tau(self):
        """Accessor for the distance to the previous node.

        Parameters
        ----------
        delta_tau : :py:class:`float`

        Returns
        -------
        delta_tau : :py:class:`float`

        Raises
        ------
        ValueError
            If ``delta_tau`` is not a :py:class:`float` and not positive.
        """
        return self._delta_tau

    @delta_tau.setter
    def delta_tau(self, delta_tau):
        assert_is_instance(delta_tau, float, descriptor="Delta Tau", checking_obj=self)
        assert_condition(delta_tau >= 0.0, ValueError,
                         message="Delta tau must be positive: NOT %f" % delta_tau,
                         checking_obj=self)
        self._delta_tau = delta_tau

    def lines_for_log(self):
        _lines = OrderedDict()
        _lines['Value'] = self.value.lines_for_log()
        _lines['Solution'] = self.solution.lines_for_log()
        _lines['Delta Tau'] = "%f" % self.delta_tau
        _lines['RHS'] = self.rhs.lines_for_log()
        _lines['Integral'] = self.integral.lines_for_log()
        return _lines

    def __str__(self):
        return "%s<0x%x>(data=%s)" % (class_name(self), id(self), self.value)

    def __repr__(self):
        return "<%s at 0x%x : data=%r>" % (class_name(self), id(self), self.value)


__all__ = ['NodeState']
