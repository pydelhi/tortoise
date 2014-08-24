from unittest import TestCase
from tortoise import Tortoise

# Test cases picked from microtemplates and 500lines


class AnyOldObject(object):

    def __init__(self, **attrs):
        for k, v in attrs.items():
            setattr(self, k, v)

    def func(self):
        return 'func!'


class TortoiseTest(TestCase):
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

    def test_simple_if_is_true(self):
        rv = Tortoise('{% if num > 5 %}\
<div>more than 5</div>\
{% endif %}').render({'num': 6})
        self.assertEquals(rv, '<div>more than 5</div>')

    def test_simple_if_is_false(self):
        rv = Tortoise('{% if num > 5 %}\
<div>more than 5</div>\
{% endif %}').render({'num': 4})
        self.assertEquals(rv, '')

    def test_if_else_if_branch(self):
        rv = Tortoise('{% if num > 5 %}\
<div>more than 5</div>\
{% else %}\
<div>less than 5</div>\
{% endif %}').render({'num': 6})
        self.assertEquals(rv, '<div>more than 5</div>')

    def test_if_else_else_branch(self):
        rv = Tortoise('{% if num > 5 %}\
<div>more than 5</div>\
{% else %}\
<div>less or equal to 5</div>\
{% endif %}').render({'num': 4})
        self.assertEquals(rv, '<div>less or equal to 5</div>')

    def test_nested_if(self):
        tmpl = '{% if num > 5 %}\
{% for foo in [1, 2] %}\
{{foo}}\
{% endfor %}\
{% else %}\
{% for bar in [3, 4] %}\
{{bar}}\
{% endfor %}\
{% endif %}'
        rv = Tortoise(tmpl).render({'num': 6})
        self.assertEquals(rv, '12')
        rv = Tortoise(tmpl).render({'num': 4})
        self.assertEquals(rv, '34')

    def test_truthy_thingy(self):
        templ = Tortoise('{% if items %}we have items{% end %}')
        self.assertEquals(templ.render({'items': []}), '')
        rv = Tortoise('{% if items %}we have items{% end %}').render({
            'items': None})
        self.assertEquals(rv, '')
        rv = Tortoise('{% if items %}we have items{% end %}').render({
            'items': ''})
        self.assertEquals(rv, '')
        rv = Tortoise('{% if items %}we have items{% end %}').render({
            'items': [1]})
        self.assertEquals(rv, 'we have items')

    def test_for_in_context(self):
        rendered = Tortoise('{% for item in items %}\
<div>{{item}}</div>\
{% endfor %}').render({'items': ['alex', 'maria']})
        self.assertEquals(rendered, '<div>alex</div><div>maria</div>')

    def test_for_as_literal_list(self):
        rendered = Tortoise('{% for item in [1, 2, 3] %}<div>\
{{item}}</div>\
{% endfor %}').render()
        self.assertEquals(rendered, '<div>1</div><div>2</div><div>3</div>')

    def test_for_parent_context(self):
        rendered = Tortoise('{% for item in [1, 2, 3] %}<div>\
{{name}}-{{item}}</div>\
{% endfor %}').render({'name': 'jon doe'})
        self.assertEquals(rendered, '<div>jon doe-1</div><div>jon doe-2</div>\
<div>jon doe-3</div>')

    def test_for_no_space(self):
        rendered = Tortoise('{% for item in [1,2, 3]%}<div>\
{{item}}</div>\
{%endfor%}').render()
        self.assertEquals(rendered, '<div>1</div><div>2</div><div>3</div>')

    def test_for_no_tags_inside(self):
        rendered = Tortoise('{% for item in [1,2,3] %}\
<br>{% endfor %}').render()
        self.assertEquals(rendered, '<br><br><br>')

    def test_nested_tag(self):
        rendered = Tortoise('{% for item in items %}\
{% if item %}\
yes\
{% endif %}\
{% endfor %}').render({'items': ['', None, '2']})
        self.assertEquals(rendered, 'yes')
