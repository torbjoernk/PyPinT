# coding=utf-8
"""Time Level
"""
from pypint.multi_level_providers.level_providers.abstract_level import AbstractLevel


class TimeLevel(AbstractLevel):
    def __init__(self, *args, **kwargs):
        super(TimeLevel, self).__init__(*args, **kwargs)

        self._integrator = None

    @property
    def integrator(self):
        return self._integrator

    @integrator.setter
    def integrator(self, value):
        self._integrator = value

    @property
    def num_nodes(self):
        return self.integrator.num_nodes

    @property
    def nodes(self):
        return self.integrator.nodes

    def lines_for_log(self):
        _lines = super(TimeLevel, self).lines_for_log()
        _lines.update({
            'Integrator': self.integrator.lines_for_log()
        })
        return _lines

    def __str__(self):
        _outstr = super(TimeLevel, self).__str__()[0:-1]
        _outstr += ", integrator=%s)" % self.integrator
        return _outstr

    def __repr__(self):
        _repr = super(TimeLevel, self).__repr__()[0:-1]
        _repr += ", integrator=%r>" % self.integrator
        return _repr


__all__ = ['TimeLevel']
