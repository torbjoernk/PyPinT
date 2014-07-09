# coding=utf-8
"""

.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
from pypint.utilities.abc import Deepcopyable
from pypint.utilities import assert_condition, class_name


class ISolution(Deepcopyable):
    """Generalized storage for solutions of solvers.
    """

    def __init__(self, *args, **kwargs):
        self._data_type = None
        self._data = None
        self._used_iterations = 0
        self._reduction = None
        self._finalized = False

    def add_solution(self, *args, **kwargs):
        """Adds a new solution data storage object.

        Raises
        ------
        NotImplementedError :
            If called directly or via :py:meth:`super`.

        Notes
        -----
        This method must be overridden in derived classes.
        """
        raise NotImplementedError("Must be implemented and overridden by subclasses.")

    def finalize(self):
        assert_condition(not self.finalized, ValueError,
                         message="Solution cannot be changed any more.", checking_obj=self)
        self._finalized = True

    @property
    def used_iterations(self):
        """Accessor for the number of iterations.

        Parameters
        ----------
        used_iterations : :py:class:`int`
            number of used iterations

        Raises
        ------
        ValueError :
            If ``used_iterations`` is not a non-zero positive integer value.

        Returns
        -------
        used_iterations : :py:class:`int`
            number of used iterations
        """
        return self._used_iterations

    @used_iterations.setter
    def used_iterations(self, used_iterations):
        assert_condition(not self.finalized, ValueError,
                         message="Solution cannot be changed any more.", checking_obj=self)
        assert_condition(used_iterations > 0, ValueError,
                         message="Number of used iterations must be non-zero positive: NOT {:d}"
                                 .format(used_iterations),
                         checking_obj=self)
        self._used_iterations = used_iterations

    @property
    def data_storage_type(self):
        """Read-only accessor for the data storage type.

        Returns
        -------
        data_storage_type : :py:class:`.TrajectorySolutionData` or :py:class:`.StepSolutionData`
            or a derived class thereof
        """
        return self._data_type

    @property
    def finalized(self):
        return self._finalized

    def __str__(self):
        return "{:s}: {}".format(class_name(self), self._data)


__all__ = ['ISolution']
