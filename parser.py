#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simplified Parser for Tortoise.
-------------------------------
A Parser's job is to generate a Parse
Tree from the stream of Tokens that it receives from
the lexer.

Lets define what a Tree is: A tree is a structure
of Nodes, each one of them having its own child
nodes. This recursive structure ends at the bottom
of the tree, where the Nodes are known as Leaves.

"""

from nodes import *
from exc import TemplateSyntaxError

# Scope stack. Push when entering a scope, pop while exiting.
# Stack size should be zero at the end of a template render.
SCOPE_STACK = []

class Parser(object):

    def __init__(self, source_text):
        self.source_text = source_text
        self.stream = Lexer(source_text)

    def create_node(self, token):
        node_cls = None
        clean_token = token.clean()

        if token.type == TOKEN_HTML:
            node_cls = HTML
        elif token.type == TOKEN_VAR:
            node_cls = Variable
        elif token.type == TOKEN_BLOCK:
            token_val = token.clean()
            if 'if' in token_val:
                node_cls = If
            elif 'for' in token_val:
                node_cls = For
            elif 'else' in token_val:
                node_cls = Else

        if node_cls:
            node = node_cls(token)
            return node
        elif not node_cls and token.type != TOKEN_BLOCK_END:
            # The end blocks are just for popping out of scope,
            # no need for actual Node objects
            raise TemplateSyntaxError("Failed to Parse token: {0}".format(token))


if __name__ == '__main__':

    source = """
<h1>Hello, {{ name }}!!</h1>
<div class="some-class">
    {% for item in list %}
        {% if item %}
            <h2> {{ item }} </h2>
        {% else %}
            <h4> {{ item }} </h4>
        {% endif %}
    {% endfor %}
</div>
"""
    parser = Parser(source)
    for token in parser.stream:
        parser.create_node(token)
