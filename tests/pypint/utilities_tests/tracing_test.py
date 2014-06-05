# coding=utf-8

import unittest
from pypint.utilities.tracing import func_name


class DummyObject(object):
    def dummy_function(self):
        return func_name(self)

    def dummy_with_args(self, a, b):
        return func_name(self, a, b)

    def dummy_with_kwargs(self, a='a', b='b'):
        return func_name(self, a=a, b=b)

    def dummy_with_args_and_kwargs(self, a, b='b'):
        return func_name(self, a, b=b)


class TracingTest(unittest.TestCase):
    def test_func_name(self):
        self.assertRegex(func_name(self), "^TracingTest<0x[0-9a-f]*>\.test_func_name\(\): $")
        self.assertRegex(func_name(), "^test_func_name\(\): $")

        self.assertRegex(DummyObject().dummy_function(), '^DummyObject<0x[0-9a-f]*>\.dummy_function\(\): $')
        self.assertRegex(DummyObject().dummy_with_args('a', 'b'),
                         '^DummyObject<0x[0-9a-f]*>\.dummy_with_args\([ab, ]{4}\): $')

        _str = DummyObject().dummy_with_kwargs()
        self.assertRegex(_str, '^DummyObject<0x[0-9a-f]*>\.dummy_with_kwargs\(.*\): $')
        self.assertRegex(_str, '.*\(.*(a=a).*\).*')
        self.assertRegex(_str, '.*\(.*(b=b).*\).*')

        _str = DummyObject().dummy_with_args_and_kwargs('a')
        self.assertRegex(_str, '^DummyObject<0x[0-9a-f]*>\.dummy_with_args_and_kwargs\(.*\): $')
        self.assertRegex(_str, '.*\(.*a{1}.*\).*')
        self.assertRegex(_str, '.*\(.*(b=b).*\).*')


if __name__ == "__main__":
    unittest.main()
