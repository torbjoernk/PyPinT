# coding=utf-8
"""Time Level
"""
import warnings

from pypint.multi_level_providers.level_providers.abstract_level import AbstractLevel
from pypint.integrators.i_integrator import IIntegrator
from pypint.utilities import assert_is_instance, func_name
from pypint.utilities.logging import LOG


class TimeLevel(AbstractLevel):
    def __init__(self, *args, **kwargs):
        super(TimeLevel, self).__init__(*args, **kwargs)

        self._integrator = None

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
