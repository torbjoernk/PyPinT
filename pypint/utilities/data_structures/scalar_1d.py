# coding=utf-8
"""
.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>
"""
import numpy as np

from pypint.utilities.data_structures.abstract_spatial_object import AbstractSpatialObject
from pypint.utilities.assertions import assert_condition, assert_is_in


class Scalar1D(AbstractSpatialObject):
    def __init__(self, *args, **kwargs):
        super(Scalar1D, self).__init__(*args, **kwargs)

        if self.dtype is None:
            self.dtype = np.dtype(np.float64)

        self._dim = 1

        self._value = self.dtype.type()
        if len(args) == 1:
            self.set(args[0])
        elif 'value' in kwargs:
            self.set(kwargs['value'])

    @property
    def value(self):
        return self._value

    @AbstractSpatialObject.dtype.setter
    def dtype(self, dtype):
        super(self.__class__, self.__class__).dtype.fset(self, dtype)
        assert_is_in(self.dtype.kind, ['i', 'u', 'f', 'c'],
                     elem_desc="Numeric Type Kind", list_desc='Valid Type Kinds',
                     checking_obj=self)

    @AbstractSpatialObject.dim.setter
    def dim(self, dim):
        raise RuntimeError("Change of dimension for Scalar1D not possible.")

    def set(self, value):
        super(Scalar1D, self).set(value)
        assert_condition(np.isscalar(value) and (np.isreal(value) or np.iscomplex(value)),
                         ValueError, message="Value must be a scalar numeric type: NOT %s" % type(value),
                         checking_obj=self)
        if not isinstance(value, self.dtype.type):
            value = self.dtype.type(value)
        self._value = value

    @property
    def norm(self):
        super(self.__class__, self.__class__).norm.fget(self)
        return self.value

    def lines_for_log(self):
        _lines = super(Scalar1D, self).lines_for_log()
        _lines['Value'] = "%s" % self.value
        return _lines

    def _get_scalar_value(self, value):
        """Returns scalar value of given value

        Returns
        -------
        In case ``value`` is an instance of :py:class:`.Scalar1D` it returns its value.
        If ``value`` is a scalar numeric type (i.e. real or complex) it returns the value itself.
        :py:class:`NotImplemented` is returned otherwise.
        """
        if isinstance(value, Scalar1D) and value.dtype.isbuiltin:
            return value.value
        elif np.isscalar(value) and (np.isreal(value) or np.iscomplex(value)):
            return value
        else:
            return NotImplemented

    def __str__(self):
        _str = super(Scalar1D, self).__str__()[0:-1]
        _str += ", value=%s)" % self.value
        return _str

    def __repr__(self):
        _repr = super(Scalar1D, self).__repr__()[0:-1]
        _repr += ", value=%s>" % self.value
        return _repr

    def __add__(self, other):
        super(Scalar1D, self).__add__(other)
        return Scalar1D(value=(self.value + self._get_scalar_value(other)), dtype=self.dtype)

    def __iadd__(self, other):
        super(Scalar1D, self).__iadd__(other)
        self._value += self._get_scalar_value(other)
        return self

    def __sub__(self, other):
        super(Scalar1D, self).__sub__(other)
        return Scalar1D(value=(self.value - self._get_scalar_value(other)), dtype=self.dtype)

    def __isub__(self, other):
        super(Scalar1D, self).__isub__(other)
        self._value -= self._get_scalar_value(other)
        return self

    def __mul__(self, other):
        super(Scalar1D, self).__mul__(other)
        if not (np.isscalar(other) and (np.isreal(other) or np.iscomplex(other))):
            return NotImplemented
        return Scalar1D(value=(self.value * other), dtype=self.dtype)

    def __imul__(self, other):
        super(Scalar1D, self).__imul__(other)
        if not (np.isscalar(other) and (np.isreal(other) or np.iscomplex(other))):
            return NotImplemented
        self._value *= other
        return self

    def __pos__(self):
        super(Scalar1D, self).__pos__()
        return Scalar1D(value=+self.value, dtype=self.dtype)

    def __neg__(self):
        super(Scalar1D, self).__neg__()
        return Scalar1D(value=-self.value, dtype=self.dtype)

    def __eq__(self, other):
        super(Scalar1D, self).__eq__(other)
        if isinstance(other, Scalar1D):
            return self.dim == other.dim and self.value == other.value
        return NotImplemented

    def __gt__(self, other):
        super(Scalar1D, self).__gt__(other)
        if isinstance(other, Scalar1D):
            return self.dim == other.dim and self.value > other.value
        return NotImplemented


__all__ = ['Scalar1D']
