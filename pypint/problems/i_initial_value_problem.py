# coding=utf-8
"""
.. moduleauthor: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np

from pypint.problems.i_problem import IProblem
from pypint.problems.transient_problem_mixin import TransientProblemMixin
from pypint.utilities import assert_condition, assert_is_instance


class IInitialValueProblem(IProblem, TransientProblemMixin):
    """Basic interface for initial value problems.

    Parameters
    ----------
    initial_value : :py:class:`numpy.ndarray`
        Initial value of :math:`u(t_0,\\phi(t_0))` with :math:`t_0` being the time interval start.
    """
    def __init__(self, *args, **kwargs):
        super(IInitialValueProblem, self).__init__(*args, **kwargs)
        TransientProblemMixin.__init__(self, *args, **kwargs)

        self._initial_value = None
        if 'initial_value' in kwargs:
            self.initial_value = kwargs['initial_value']

    @property
    def initial_value(self):
        """Accessor for the initial value.

        Parameters
        ----------
        initial_value : :py:class:`numpy.ndarray`
            Initial value of the solution.

        Returns
        -------
        initial_value : :py:class:`numpy.ndarray`
            Initial value of the solution.

        Raises
        ------
        ValueError

            * if ``initial_value`` is not a :py:class:`numpy.ndarray` with shape of :py:attr:`.IProblem.dim`
            * if ``initial_value``'s size is not equal the number of spacial :py:attr:`.IProblem.dim`
        """
        return self._initial_value

    @initial_value.setter
    def initial_value(self, initial_value):
        assert_is_instance(initial_value, np.ndarray, descriptor="Initial Value", checking_obj=self)
        assert_condition(initial_value.shape == self.dim_for_time_solver, ValueError,
                         message="Initial Values shape must match problem DOFs: %s != %s"
                                 % (initial_value.shape, self.dim_for_time_solver),
                         checking_obj=self)
        self._initial_value = initial_value

    def print_lines_for_log(self):
        _lines = super(IInitialValueProblem, self).print_lines_for_log()
        _lines.update(TransientProblemMixin.print_lines_for_log(self))
        _lines['Initial Value'] = 'u({:.3f}) = {}'.format(self.time_start, self.initial_value)
        return _lines

    def __str__(self):
        _out = super(IInitialValueProblem, self).__str__()
        _out += TransientProblemMixin.__str__(self)
        _out += r", u({:.2f})={}".format(self.time_start, self.initial_value)
        return _out


__all__ = ['IInitialValueProblem']
