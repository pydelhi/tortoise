from lexer import Lexer
from tokens import *
from utils import resolve, eval_expression

import re


class _Node(object):
    """
    Take a Token and make a Node item out of it,
    each node has a parent and multiple children.
    """
    # Each node has its own allowed fields, which could be
    # other nodes, lists or any other type of value.

    creates_scope = False

    def __init__(self, token=None):
        self.token = token
        self.children = []

    def process_token(self):
        raise NotImplementedError

    def render_children(self, context, children=None):
        if children is None:
            children = self.children

        def render_child(child):
            child_html = child.render(context)
            return '' if not child_html else str(child_html)

        # Render all the children!
        return ''.join(map(render_child, children))

    def render(self, context):
        raise NotImplementedError

    def enter_scope(self):
        raise NotImplementedError

    def exit_scope(self):
        raise NotImplementedError


    def __repr__(self):
        return '<Node {0}>'.format(self.__class__.__name__)

class _ScopedNode(_Node):
    creates_scope = True


class Root(_Node):

    def render(self, context):
        return self.render_children(context)


class Variable(_Node):

    def process_token(self, token=None):
        if token.type == TOKEN_VAR:
            return token.value
        else:
            raise TypeError

    def render(self, context):
        return resolve(self.token.value, context)


class For(_ScopedNode):
    """
    For loop:
        - Target: target for the iteration, a name or a tuple.
        - Iterable.
        - Body: list of nodes in loop body.
        - Else: list of nodes for the else block.
    """
    def process_token(self, token):
        """
        :token: for i in [1, 2, 3]
        :token: for i in ('a', 'b', 'c')
        """
        try:
            _, _iter = literal_eval(re.split('\s+', token, 1))
        except ValueError:
            raise SyntaxError(token)

    def render(self, context):
        if _iter[0] == 'literal':
            items = _iter[1]
        elif _iter[0] == 'name':
            items = resolve(iter[1], context)

        def render_item(item):
            return self.render_children(context, self.children)

        return ''.join(map(render_item, items))


class If(_ScopedNode):

    def process_token(self, token):
        pass

    def render(self, context):
        pass


class Else(_ScopedNode):

    def process_token(self, token):
        pass

    def render(self, context):
        pass


class HTML(_Node):

    def process_token(self, token):
        self.token = token

    def render(self, context):
        return self.token

