from lexer import Lexer
from tokens import *
from utils import resolve, eval_expression
from exc import TemplateSyntaxError
from syntax import OP_TABLE

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
        self.process_token(self.token)

    def process_token(self, token):
        pass

    def render_children(self, context, children=None):
        if children is None:
            children = self.children

        def render_child(child):
            child_html = child.render(context)
            return '' if child_html is None else str(child_html)

        # Render all the children!
        return ''.join(map(render_child, children))

    def render(self, context):
        pass

    def enter_scope(self):
        pass

    def exit_scope(self):
        pass

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
        return resolve(self.token.clean(), context)


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
        # Evaluate the iterable and then render
        # the result items individually.
        try:
            loop = re.split('\s+', token.clean(), 3)
            if len(loop) != 4 or loop[2] != 'in':
                raise TemplateSyntaxError('Invalid for loop expression!')
            else:
                self._loop_var = loop[1]
                iterable = loop[-1]
                # Add the variable name to the current scope
            self._iter = eval_expression(iterable)
        except ValueError:
            raise SyntaxError(token)

    def render(self, context):
        if self._iter[0] == 'literal':
            items = self._iter[1]
        elif self._iter[0] == 'name':
            items = resolve(self._iter[1], context)

        # Since Py2.x can't mutate parent scope variables,
        # we use a dictionary to pass in the index to the function below.
        nonlocals = {'index': 0}

        def render_item(item):
            # Add the current item to be rendered into the context.
            context[self._loop_var] = item
            context['index'] = nonlocals['index']
            nonlocals['index'] += 1
            return self.render_children(context, self.children)

        return ''.join(map(render_item, items))


class If(_ScopedNode):

    def process_token(self, token):
        """
        :token: if (test)
        """
        try:
            self.conditional = re.split('\s+', token.clean(), 4)
            length = len(self.conditional)
            if length != 2 and length != 4 and length != 5:
                raise TemplateSyntaxError('Invalid If expression!')
        except ValueError:
            raise SyntaxError(token)

    def render(self, context):
        self._ctx = context
        self._test = self.eval_condition(self.conditional)
        else_node = self.check_else(self.conditional)
        children = None
        render = True
        if self._test:
            children = self.children
        elif else_node and not self._test:
            children = else_node.children
        else:
            render = False
        if render:
            rendered_children = self.render_children(context, children)
            return ''.join(rendered_children)

    def check_else(self, cond):
        for item in self.children:
            if isinstance(item, Else):
                return item

    def resolve_in_expression(self, expr, ctx):
        expr_type, expr = eval_expression(expr)
        if expr_type == 'name' and expr:
            resolved = resolve(expr, ctx)
            return eval_expression(resolved)[1] if resolved else None
        elif expr_type == 'literal':
            return expr

    def eval_condition(self, cond):
        ctx = self._ctx
        # cond[0] will be the token, skip.
        left = self.resolve_in_expression(cond[1], ctx)
        right = self.resolve_in_expression(cond[-1], ctx)
        if len(cond) == 4:
            op = OP_TABLE.get(cond[2], None)
            if not op and cond[2] != 'is':
                raise TemplateSyntaxError('Invalid operator: {}'.format(
                    cond[2]))
            elif cond[2] == 'is':
                return bool(left is right)
            return op(left, right)
        if len(cond) == 5:
            if cond[2] != 'is' or cond[3] != 'not':
                raise TemplateSyntaxError('Invalid If expression!')
            else:
                return bool(left is not right)
        return bool(right)


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
