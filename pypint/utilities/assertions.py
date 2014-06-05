# coding=utf-8
"""Collection of assertions for validation.

.. moduleauthor:: Torbjörn Klatt <t.klatt@fz-juelich.de>

Examples
--------
>>> a = 3
>>> b = 2
>>> assert_condition(3 > 2, ValueError, "3 should be larger 2")

>>> func = lambda x: x
>>> assert_is_callable(func, "A lambda expression is callable.")

>>> l = [1, 2, 4]
>>> assert_is_in(2, l, "2 is in the list")

>>> m = {'hello': 'world'}
>>> assert_is_key('hello', m, "'hello' is a key")

>>> a = 1
>>> assert_is_instance(a, int, "'a' is an integer")
"""
import inspect
from collections import Callable

from pypint.utilities.tracing import class_name
from pypint.utilities.logging import LOG


def assert_condition(condition, exception_type, message, checking_obj=None):
    """Asserts trueness of arbitrary condition

    Parameters
    ----------
    condition : :py:class:`bool` or ``boolean expression``
        expression to be asserted
    exception_type : :py:class:`Exception`
        type of exception to be raised if ``condition`` evaluates to :py:class:`False`
    message : :py:class:`str`
        message content of exception raised
    checking_obj : :py:class:`object` or :py:class:`None`
        The exception will be raised in the scope of the given object.
        If :py:class:`None` (default) no scope will be displayed.

    Raises
    ------
    exception_type
        if ``condition`` evaluates to :py:class:`False`
    """
    if not condition:
        _calling_func = inspect.stack()[1][3]
        _prefix = "%s." % class_name(checking_obj) if checking_obj is not None else ''
        LOG.critical("%s%s(): %s" % (_prefix, _calling_func, message))
        raise exception_type("%s%s(): %s" % (_prefix, _calling_func, message))


def assert_is_callable(obj, message=None, descriptor=None, checking_obj=None):
    """Asserts callability of given object

    Parameters
    ----------
    obj : :py:class:`object`
        object to be asserted callable
    message : :py:class:`str` or :py:class:`None`
        *(optional)*
    checking_obj : :py:class:`object` or :py:class:`None`
        *(optional)*
        The exception will be raised in the scope of the given object.
        If :py:class:`None` (default) no scope will be displayed.

    Raises
    ------
    ValueError
        if ``obj`` is not :py:class:`Callable`
    """
    if not isinstance(obj, Callable):
        if not message:
            if descriptor:
                message = "%s must be callable." % descriptor
            else:
                message = "Required a callable: NOT %s." % class_name(obj)
        _calling_func = inspect.stack()[1][3]
        _prefix = "%s." % class_name(checking_obj) if checking_obj is not None else ''
        LOG.critical("%s%s(): %s" % (_prefix, _calling_func, message))
        raise ValueError("%s%s(): %s" % (_prefix, _calling_func, message))


def assert_is_in(element, test_list, message=None, elem_desc=None, list_desc=None, checking_obj=None):
    """Asserts element in list or sequence

    Parameters
    ----------
    element : :py:class:`object`
        element to check membership
    test_list : ``Sequence``
        sequence to check
    message : :py:class:`str`
        *(optional)*
        message content of exception raised
    checking_obj : :py:class:`object` or :py:class:`None`
        *(optional)*
        The exception will be raised in the scope of the given object.
        If :py:class:`None` (default) no scope will be displayed.

    Raises
    ------
    ValueError
        if ``element`` is not in ``test_list``

    Examples
    --------
    assert_is_in(True, bool_list, elem_desc='', list_desc='', checking_obj=self)

    """
    if element not in test_list:
        if not message:
            if not list_desc:
                list_desc = class_name(test_list)
            if not elem_desc:
                elem_desc = "Element %r" % element
            message = "%s is not in %s." % (elem_desc, list_desc)
        _calling_func = inspect.stack()[1][3]
        _prefix = "%s." % class_name(checking_obj) if checking_obj is not None else ''
        LOG.critical("%s%s(): %s" % (_prefix, _calling_func, message))
        raise ValueError("%s%s(): %s" % (_prefix, _calling_func, message))


def assert_is_instance(obj, instances, message=None, descriptor=None, checking_obj=None):
    """Asserts element is of certain type

    Parameters
    ----------
    obj : :py:class:`object`
        object to check type
    instances : :py:class:`type` of ``classes`` or :py:class:`class`
        types to check
    message : :py:class:`str`
        *(optional)*
        message content of exception raised
    checking_obj : :py:class:`object` or :py:class:`None`
        *(optional)*
        The exception will be raised in the scope of the given object.
        If :py:class:`None` (default) no scope will be displayed.

    Raises
    ------
    ValueError
        if ``obj`` is not of type ``instances``
    """
    if not isinstance(obj, instances):
        if not message:
            _instances_str = set()
            if isinstance(instances, (tuple, set, frozenset)):
                for _i in instances:
                    _instances_str.add("'%s'" % _i.__name__)
            else:
                _instances_str.add("'%s'" % instances.__name__)

            if descriptor:
                if len(_instances_str) > 1:
                    message = "%s must be one of %s: NOT %s." \
                              % (descriptor, ', '.join(_instances_str), class_name(obj))
                else:
                    message = "%s must be a %s: NOT %s." \
                              % (descriptor, ', '.join(_instances_str), class_name(obj))
            else:
                if len(_instances_str) > 1:
                    message = "Required one of %s: NOT %s." % (', '.join(_instances_str), class_name(obj))
                else:
                    message = "Required a %s: NOT %s." % (', '.join(_instances_str), class_name(obj))
        _calling_func = inspect.stack()[1][3]
        _prefix = "%s." % class_name(checking_obj) if checking_obj is not None else ''
        LOG.critical("%s%s(): %s" % (_prefix, _calling_func, message))
        raise ValueError("%s%s(): %s" % (_prefix, _calling_func, message))


def assert_is_key(key, dictionary, message=None, key_desc=None, dict_desc=None, checking_obj=None):
    """Asserts dictionary has a certain key

    Parameters
    ----------
    key : ``key``
        key to check
    dictionary : :py:class:`dict`
        dictionary to check
    message : :py:class:`str`
        *(optional)*
        message content of exception raised
    checking_obj : :py:class:`object` or :py:class:`None`
        *(optional)*
        The exception will be raised in the scope of the given object.
        If :py:class:`None` (default) no scope will be displayed.

    Raises
    ------
    ValueError
        if ``key`` is not of a key in ``dictionary``
    """
    if key not in dictionary:
        if not message:
            if key_desc is None:
                key_desc = "'%s'" % key
            if dict_desc is None:
                dict_desc = "given dict"
            message = "%s is not a key in %s." % (key_desc, dict_desc)
        _calling_func = inspect.stack()[1][3]
        _prefix = "%s." % class_name(checking_obj) if checking_obj is not None else ''
        LOG.critical("%s%s(): %s" % (_prefix, _calling_func, message))
        LOG.debug("%s%s(): Keys in %s: %s" % (_prefix, _calling_func, id(dictionary), ', '.join(dictionary.keys())))
        raise ValueError("%s%s(): %s" % (_prefix, _calling_func, message))


def assert_named_argument(name, kwargs, types=None, message=None, descriptor=None, checking_obj=None):
    if name not in kwargs:
        if not message:
            if descriptor:
                message = "%s ('%s') is a required argument." % (descriptor, name)
            else:
                message = "'%s' is a required argument." % name
        _calling_func = inspect.stack()[1][3]
        _prefix = "%s." % class_name(checking_obj) if checking_obj is not None else ''
        LOG.critical("%s%s(): %s" % (_prefix, _calling_func, message))
        LOG.debug("%s%s(): Named arguments were: %s" % (_prefix, _calling_func, ', '.join(kwargs.keys())))
        raise ValueError("%s%s(): %s" % (_prefix, _calling_func, message))

    if types:
        assert_is_instance(kwargs[name], types, descriptor=descriptor, checking_obj=checking_obj)


__all__ = [
    'assert_condition',
    'assert_is_callable',
    'assert_is_in',
    'assert_is_instance',
    'assert_is_key',
    'assert_named_argument'
]
