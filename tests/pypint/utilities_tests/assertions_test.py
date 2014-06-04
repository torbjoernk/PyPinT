# coding=utf-8
import unittest

from pypint.utilities.assertions \
    import assert_condition, assert_is_callable, assert_is_in, assert_is_instance, assert_is_key, assert_named_argument


class Dummy(object):
    def condition(self):
        assert_condition(False, ValueError, message='msg', checking_obj=self)

    def callable(self):
        assert_is_callable(3, checking_obj=self)

    def in_list(self):
        assert_is_in(3, [1, 2], checking_obj=self)

    def instance(self):
        assert_is_instance(3.1, int, checking_obj=self)

    def is_key(self):
        assert_is_key('not a key', {'key': 3}, key_desc='KEY', dict_desc='DICT', checking_obj=self)

    def named_argument(self, **kwargs):
        assert_named_argument('kwarg', kwargs, types=str, descriptor='ARGUMENT', checking_obj=self)


class AssertionsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_assert_condition(self):
        assert_condition(True, ValueError, message='msg')

        with self.assertRaisesRegex(ValueError, '^test_assert_condition\(\): msg'):
            assert_condition(False, ValueError, message='msg')

        with self.assertRaisesRegex(ValueError, '^Dummy.condition\(\): msg'):
            Dummy().condition()

    def test_assert_is_callable(self):
        assert_is_callable(lambda x: x)

        with self.assertRaisesRegex(ValueError, '^test_assert_is_callable\(\): Required a callable: NOT int\.'):
            assert_is_callable(3)

        with self.assertRaisesRegex(ValueError, '^test_assert_is_callable\(\): Descriptor must be callable\.'):
            assert_is_callable(3, descriptor='Descriptor')

        with self.assertRaisesRegex(ValueError, '^Dummy.callable\(\): Required a callable: NOT int\.'):
            Dummy().callable()

    def test_assert_is_in(self):
        assert_is_in(3, [1, 2, 3])

        with self.assertRaisesRegex(ValueError, '^test_assert_is_in\(\): Element 3 is not in list\.'):
            assert_is_in(3, [1, 2])

        with self.assertRaisesRegex(ValueError, '^test_assert_is_in\(\): Number is not in Given List\.'):
            assert_is_in(3, [1, 2], elem_desc='Number', list_desc='Given List')

        with self.assertRaisesRegex(ValueError, '^Dummy.in_list\(\): Element 3 is not in list\.'):
            Dummy().in_list()

    def test_assert_is_instance(self):
        assert_is_instance(3, int)
        assert_is_instance(3, (int, float))

        with self.assertRaisesRegex(ValueError, '^test_assert_is_instance\(\): Required a \'int\': NOT float\.'):
            assert_is_instance(3.1, int)
        with self.assertRaisesRegex(ValueError, '^test_assert_is_instance\(\): Required one of .*: NOT float\.'):
            assert_is_instance(3.1, (int, str))

        with self.assertRaisesRegex(ValueError, '^test_assert_is_instance\(\): Number must be a \'int\': NOT float\.'):
            assert_is_instance(3.1, int, descriptor='Number')
        with self.assertRaisesRegex(ValueError, '^test_assert_is_instance\(\): Number must be one of .*: NOT float\.'):
            assert_is_instance(3.1, (int, str), descriptor='Number')

        with self.assertRaisesRegex(ValueError, '^Dummy.instance\(\): Required a \'int\': NOT float\.'):
            Dummy().instance()

    def test_assert_is_key(self):
        assert_is_key('key', {'key': 3})

        with self.assertRaisesRegex(ValueError, '^test_assert_is_key\(\): \'not a key\' is not a key in given dict\.'):
            assert_is_key('not a key', {'key': 3})

        with self.assertRaisesRegex(ValueError, '^test_assert_is_key\(\): msg'):
            assert_is_key('not a key', {'key': 3}, message='msg')
        with self.assertRaisesRegex(ValueError, '^test_assert_is_key\(\): KEY is not a key in given dict\.'):
            assert_is_key('not a key', {'key': 3}, key_desc='KEY')
        with self.assertRaisesRegex(ValueError, '^test_assert_is_key\(\): KEY is not a key in DICT\.'):
            assert_is_key('not a key', {'key': 3}, key_desc='KEY', dict_desc='DICT')

        with self.assertRaisesRegex(ValueError, '^Dummy.is_key\(\): KEY is not a key in DICT\.'):
            Dummy().is_key()

    def test_assert_named_argument(self):
        assert_named_argument('kwarg', {'kwarg': 'value'})

        with self.assertRaisesRegex(ValueError, '^test_assert_named_argument\(\): \'kwarg\' is a required argument\.'):
            assert_named_argument('kwarg', {'not kwarg': 'value'})
        with self.assertRaisesRegex(ValueError,
                                    '^test_assert_named_argument\(\): ARG \(\'kwarg\'\) is a required argument\.'):
            assert_named_argument('kwarg', {'not kwarg': 'value'}, descriptor='ARG')
        with self.assertRaisesRegex(ValueError, '^test_assert_named_argument\(\): msg'):
            assert_named_argument('kwarg', {'not kwarg': 'value'}, message='msg')

        with self.assertRaisesRegex(ValueError, '^assert_named_argument\(\): Required a \'int\': NOT str\.'):
            assert_named_argument('kwarg', {'kwarg': 'not int'}, types=int)

        with self.assertRaisesRegex(ValueError,
                                    '^Dummy.named_argument\(\): ARGUMENT \(\'kwarg\'\) is a required argument\.'):
            Dummy().named_argument()


if __name__ == '__main__':
    unittest.main()
