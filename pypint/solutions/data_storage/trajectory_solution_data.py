# coding=utf-8
"""

.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import warnings
from copy import deepcopy
from collections import OrderedDict
from collections.abc import MutableSequence

import numpy as np

from pypint.solutions.data_storage.step_solution_data import StepSolutionData
from pypint.utilities.abc import Deepcopyable
from pypint.utilities.assertions import assert_condition, assert_is_in, assert_is_instance


class TrajectorySolutionData(MutableSequence, Deepcopyable):
    """Storage for a transient trajectory of solutions.

    Basically, this is nothing more than an array of :py:class:`.StepSolutionData` objects and a couple of
    utility functions for easy data access and consistency checks.
    """

    def __init__(self):
        self._data = []
        self._time_points = []
        self._dtype = None
        self._dim = None
        self._finalized = False

    def add_solution_data(self, *args, **kwargs):
        """Appends solution of a new time point to the trajectory.

        Parameters
        ----------
        step_data : :py:class:`.StepSolutionData`
            *(optional)*
            In case a single unnamed argument is given, this is required to be an instance of
            :py:class:`.StepSolutionData`.

            index : :py:class:`integer`
                *(optional)*
                List index of the to-be-added step data.

            If no named argument is given, the following two parameters are *not* optional.
        values : :py:class:`numpy.ndarray`
            *(optional)*
            Solution values.
            Passed on to constructor of :py:class:`.StepSolutionData`.
        time_point : :py:class:`float`
            *(optional)*
            Time point of the solution.
            Passed on to constructor of :py:class:`.StepSolutionData`.

        Raises
        ------
        ValueError

            * if construction of :py:class:`.StepSolutionData` fails
            * if internal consistency check fails (see :py:meth:`._check_consistency`)
        """
        assert_condition(not self.finalized, AttributeError,
                         message="Cannot change this solution data storage any more.", checking_obj=self)
        _old_data = deepcopy(self._data)  # backup for potential rollback

        if len(args) == 1 and isinstance(args[0], StepSolutionData):
            assert_condition(args[0].time_point is not None, ValueError,
                             message="Time point must not be None.", checking_obj=self)
            if 'index' not in kwargs:
                self._data.append(args[0])
            else:
                self._data.insert(kwargs.get('index'), args[0])
        else:
            self._data.append(StepSolutionData(*args, **kwargs))

        try:
            self._check_consistency()
        except ValueError as err:
            # consistency check failed, thus removing recently added solution data storage
            warnings.warn("Consistency Check failed with:\n\t\t{}\n\tNot adding this solution.".format(*err.args))
            self._data = _old_data  # rollback
            raise err
        finally:
            # everything ok
            pass

        self._time_points = [step.time_point for step in self.data]

        if len(self._data) == 1:
            self._dim = self._data[0].dim
            self._dtype = self._data[0].dtype

    def finalize(self):
        """Locks this storage data instance.

        Raises
        ------
        ValueError :
            If it has already been locked.
        """
        assert_condition(not self.finalized, AttributeError,
                         message="This solution data storage is already finalized.", checking_obj=self)
        self._finalized = True

    def at(self, time_point):
        """Retrieve data at a given time point

        Parameters
        ----------
        time_point : :py:class:`float`
            time point of the solution data to retrieve

        Returns
        -------
        data : py:class:`.StepSolutionData` or :py:class:`None`
            :py:class:`None` is returned iff `time_point` is not in :py:attr:`.time_points`
        """
        if time_point in self._time_points:
            return self._data[self._time_points.index(time_point)]
        else:
            return None

    def set_at(self, time_point, data):
        assert_is_in(time_point, self._time_points, elem_desc='Time Point', list_desc='Available Time Points',
                     checking_obj=self)
        assert_is_instance(data, StepSolutionData, descriptor='Solution Data', checking_obj=self)
        _old_data = deepcopy(self._data)
        self._data[self._time_points.index(time_point)] = data
        try:
            self._check_consistency()
        except ValueError as err:
            # consistency check failed, thus removing recently added solution data storage
            warnings.warn("Consistency Check failed with:\n\t\t{}\n\tNot adding this solution.".format(*err.args))
            self._data = _old_data  # rollback
            raise err
        finally:
            # everything ok
            pass

    @property
    def finalized(self):
        """Accessor for the lock state.

        Returns
        -------
        finilized : :py:class:`bool`
            :py:class:`True` if it has been finalized before, :py:class:`False` otherwise
        """
        return self._finalized

    @property
    def data(self):
        """Read-only accessor for the stored solution objects.

        Returns
        -------
        data : :py:class:`numpy.ndarray` of :py:class:`.StepSolutionData`
        """
        return self._data

    @property
    def time_points(self):
        """Accessor for the time points of stored solution data.

        Returns
        -------
        error : :py:class:`numpy.ndarray` of :py:class:`float`
        """
        return np.asarray(self._time_points, dtype=np.float)

    @property
    def values(self):
        """Accessor for the solution values of stored solution data.

        Returns
        -------
        error : :py:class:`numpy.ndarray` of :py:class:`.numeric_type`
        """
        return np.asarray([step.value for step in self.data], dtype=np.object)

    @property
    def errors(self):
        """Accessor for the errors of stored solution data.

        Returns
        -------
        error : :py:class:`numpy.ndarray` of :py:class:`.Error`
        """
        return np.asarray([step.error for step in self.data], dtype=np.object)

    @property
    def residuals(self):
        """Accessor for the residuals of stored solution data.

        Returns
        -------
        error : :py:class:`numpy.ndarray` of :py:class:`.Residual`
        """
        return np.asarray([step.residual for step in self.data], dtype=np.object)

    @property
    def dtype(self):
        """Read-only accessor for the numeric type of the solution data values.
        """
        return self._dtype

    @property
    def dim(self):
        """Read-only accessor for the spacial dimension of the solution data values.
        """
        return self._dim

    def _check_consistency(self):
        """Checks for consistency of spacial dimension and numeric type of stored steps.

        Raises
        ------
        ValueError :

            * if the time points of the steps are not strictly increasing
            * if the numeric type of at least one step does not match :py:attr:`.dtype`
            * if the spacial dimension of at least one step does not match :py:attr:`.dim`
        """
        if len(self._data) > 0:
            _time_point = self.data[0].time_point
            for step_index in range(1, len(self.data)):
                assert_condition(self.data[step_index].time_point > _time_point, ValueError,
                                 message="Time points must be strictly increasing: %f <= %f"
                                         % (self.data[step_index].time_point, _time_point),
                                 checking_obj=self)
                assert_condition(self.data[step_index].dtype == self.dtype,
                                 ValueError,
                                 message=("Numeric type of step %d does not match global numeric type: %s"
                                          % (step_index, self.dtype) +
                                          "%s != %s" % (self.data[step_index].dtype, self.dtype)),
                                 checking_obj=self)
                assert_condition(self.data[step_index].dim == self.dim,
                                 ValueError,
                                 message=("Spacial dimension of step %d does not match global spacial dimension: %s"
                                          % (step_index, self.dim) +
                                          "%s != %s" % (self.data[step_index].dim, self.dim)),
                                 checking_obj=self)

    def insert(self, index, value):
        self.add_solution_data(value, index=index)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self.set_at(index, value)

    def __delitem__(self, index):
        if 0 <= abs(index) < len(self._data) and 0 <= abs(index) < len(self._time_points):
            del self._time_points[index]
            del self._data[index]
        else:
            raise IndexError

    def lines_for_log(self):
        _lines = OrderedDict()
        _lines['Data'] = [item.lines_for_log() for item in self.data]
        _lines['Time Points'] = "%s" % self._time_points
        return _lines

    def __str__(self):
        return "TrajectorySolutionData<0x%x>(data=%s, time_points=%s)" % (id(self), self.data, self.time_points)

    def __repr__(self):
        return "<TrajectorySolutionData at 0x%x : data=%s, time_points=%s>" % (id(self), self.data, self.time_points)


__all__ = ['TrajectorySolutionData']
