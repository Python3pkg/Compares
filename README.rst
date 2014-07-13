========
Compares
========

``Compares`` is a module that defines a single decorator, ``compares.via``\ ,
which removes some boilerplate around defining ``__eq__``\ , ``__ne__`` and
``__repr__`` for object comparisons and display.

It takes advantage of the fact that there is often a set of relevant attributes
(fields) which should be used to compare instances.

It is inspired by `twisted.python.util.FancyEqMixin
<https://twistedmatrix.com/documents/current/api/twisted.python.util.FancyEqMixin.html>`_\ .


Usage
-----

.. code-block:: python

    >>> import compares
    >>> @compares.via(("foo", "bar"))
    ... class Foo(object):
    ...     def __init__(self, foo, bar, baz):
    ...         self.foo = foo
    ...         self.bar = bar
    ...         self.baz = baz

    >>> foo = Foo(foo=12, bar=13, baz=14)
    >>> assert foo == Foo(foo=12, bar=13, baz="YEP")
    >>> assert not foo == Foo(foo="NOPE", bar=13, baz="")
    >>> assert repr(foo) == "<Foo foo=12 bar=13>"
