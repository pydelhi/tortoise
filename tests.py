from unittest import TestCase
from tortoise import Tortoise


class AnyOldObject(object):

    def __init__(self, **attrs):
        for k, v in attrs.items():
            setattr(self, k, v)


class TemplateTest(TestCase):

    def try_render(self, text, ctx=None, result=None):
        """
        Render `test` through `ctx` and it had better be `result`.

        Results default to None so we can shorten the calls where
        we expect an exception and never get to the result comparison.
        """
        actual = Tortoise(text).render(ctx or {})
        if result:
            self.assertEqual(result, actual)

    def test_passthrough(self):
        """
        Strigs without variables are passed through unchanged.
        """
        self.assertEqual(Tortoise("Hello").render(), "Hello")
        self.assertEqual(
            Tortoise("Hello, 20% fun time!").render(),
            "Hello, 20% fun time!"
        )

    def test_variables(self):
        # Variables use {{ var }} syntax
        self.try_render("Hello, {{ name }}", ctx={'name': 'Manish'},
                        result="Hello, Manish")

    def test_undefined_variables(self):
        with self.assertRaises(Exception):
            self.try_render("Hi, {{ name }}!")

    def test_reusability(self):
        # A single template can be used more than once with different data
        template = Tortoise("This is {{ name }}")
        self.assertEqual(template.render({'name': 'Foo'}), 'This is Foo')
        self.assertEqual(template.render({'name': 'Bar'}), 'This is Bar')

    def test_attribute(self):
        # Variables' attributes can be accessed with dots
        obj = AnyOldObject(a="Any")
        self.try_render("{{ obj.a }}", locals(), "Any")
        self.try_render("{{ obj.func }}", locals(), "func!")

        obj2 = AnyOldObject(obj=obj, b="Bee")
        self.try_render("{{obj2.obj.a}} {{ obj2.b }}", locals(), "Any Bee")

