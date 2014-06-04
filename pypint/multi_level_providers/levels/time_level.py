# coding=utf-8
"""Time Level
"""
import warnings

from numpy import ndarray

from pypint.multi_level_providers.levels.abstract_level import AbstractLevel
from pypint.integrators.i_integrator import IIntegrator
from pypint.utilities import assert_is_instance, func_name
from pypint.utilities.logging import LOG


class TimeLevel(AbstractLevel):
    """Representation of a Time Level

    Without knowledge of spacial dimensions.
    Holds a time integrator.

    Parameters
    ----------
    integrator : :py:class:`.IIntegrator`
        *(optional)*
        time integrator to be used; see :py:attr:`.integrator`
    """
    def __init__(self, *args, **kwargs):
        super(TimeLevel, self).__init__(*args, **kwargs)

        self._integrator = None
        if 'integrator' in kwargs:
            self.integrator = kwargs.get('integrator')

    def validate_data(self, data):
        """
        Returns
        -------
        data_valid : :py:class:`bool`
            :py:class:`False` if ``data`` is not a :py:class:`list` or :py:class:`numpy.ndarray` with
            :py:attr:`.num_nodes` elements and all elements are instances of the same class;
            :py:class:`False` otherwise.
        """
        super(TimeLevel, self).validate_data(data)
        if isinstance(data, (list, ndarray)):
            if len(data) == self.num_nodes:
                return all(elem.__class__ is data[0].__class__ for elem in data)
            else:
                warnings.warn("Given data has incompatible length: %s != %s" % (len(data), self.num_nodes))
                LOG.warn("%sGiven data has incompatible length: %s != %s"
                         % (func_name(self), len(data), self.num_nodes))
                return False
        else:
            warnings.warn("Given data is of incompatible type: NOT %s" % type(data))
            LOG.warn("%sGiven data is of incompatible type: NOT %s" % (func_name(self), type(data)))
            return False

    @property
    def integrator(self):
        return self._integrator

    @integrator.setter
    def integrator(self, value):
        assert_is_instance(value, IIntegrator, descriptor="Integrator", checking_obj=self)
        self._integrator = value

    @property
    def num_nodes(self):
        if self.integrator is None:
            warnings.warn("Integrator not set.")
            LOG.warn("%sIntegrator is not set." % func_name(self))
            return None
        return self.integrator.num_nodes

    @property
    def nodes(self):
        if self.integrator is None:
            warnings.warn("Integrator not set.")
            LOG.warn("%sIntegrator is not set." % func_name(self))
            return None
        return self.integrator.nodes

    def lines_for_log(self):
        _lines = super(TimeLevel, self).lines_for_log()
        _lines.update({
            'Integrator': self.integrator.lines_for_log() if self.integrator is not None else None
        })
        return _lines

    def __str__(self):
        _outstr = super(TimeLevel, self).__str__()[0:-1]
        _outstr += "integrator=%s)" % self.integrator
        return _outstr

    def __repr__(self):
        _repr = super(TimeLevel, self).__repr__()[0:-1]
        _repr += " : integrator=%r>" % self.integrator
        return _repr


__all__ = ['TimeLevel']
