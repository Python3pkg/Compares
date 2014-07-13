import sys

if sys.version_info[:2] <= (2, 6):
    from unittest2 import TestCase
else:
    from unittest import TestCase

import compares


@compares.via(fields=("foo", "bar"))
class Foo(object):
    def __init__(self, foo, bar, baz=14):
        self.foo = foo
        self.bar = bar
        self.baz = baz


class HasARepr(object):
    def __repr__(self):
        return "HI"


class TestComparesVia(TestCase):
    def test_fields(self):
        self.assertEqual(Foo(foo=12, bar=u"Hello").fields, ("foo", "bar"))

    def test_repr(self):
        self.assertEqual(
            repr(Foo(foo=12, bar=HasARepr())), "<Foo foo=12 bar=HI>",
        )

    def test_eq(self):
        self.assertTrue(Foo(foo=12, bar=u"yes") == Foo(foo=12, bar=u"yes"))
        self.assertFalse(Foo(foo=12, bar=u"no") == Foo(foo=12, bar=u"yes"))

    def test_ne(self):
        self.assertTrue(Foo(foo=12, bar=u"no") != Foo(foo=12, bar=u"yes"))
        self.assertFalse(Foo(foo=12, bar=u"yes") != Foo(foo=12, bar=u"yes"))

    def test_eq_does_not_know_about_random_objects(self):
        self.assertIs(
            Foo(foo=12, bar=u"Hello").__eq__(object()), NotImplemented,
        )

    def test_ne_does_not_know_about_random_objects(self):
        self.assertIs(
            Foo(foo=12, bar=u"Hello").__ne__(object()), NotImplemented,
        )

    def test_contents(self):
        self.assertEqual(
            Foo(foo=12, bar=u"yes")._contents, [("foo", 12), ("bar", u"yes")],
        )

    def test_it_detects_if_the_class_defines_some_attributes_already(self):
        @compares.via(fields=("foo",))
        class Foo(object):

            fields = "COFFEE"
            _compares = 12

            def __repr__(self):
                return "123"

        self.assertEqual(Foo.fields, "COFFEE")
        self.assertEqual(Foo._compares, 12)
        self.assertEqual(repr(Foo()), "123")
