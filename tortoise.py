import parser


class Tortoise(object):

    def __init__(self, text):
        self.text = text
        self.root = parser.Parser(self.text).generate_parse_tree()

    def render(self, ctx=None):
        ctx = ctx or {}
        return self.root.render(ctx)


if __name__ == '__main__':
    text = """
Hello, {{ name }}.
{% for item in [1, 2, 3] %}
    Index {{ index }}: {{ item }}
    {% if myList %}
        do something here
    {% else %}
        do something else
    {% endif %}
{% endfor %}"""
    context = {"name": "Manish", "myList": [1, 1, 2, 3, 5, 8]}
    template = Tortoise(text)
    print(template.render(context))
