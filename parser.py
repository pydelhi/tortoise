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
from tokens import *
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


    def generate_parse_tree(self):
        """
        1. Start from the Root Node.
        2. Obtain next token in stream.
        3. If token is end type, pop indicator out of scope.
        3a. End token should know how many branches are to be popped out of stack.
        4. Create new node from that token.
        5. If Node is scopable, push indicator into scope stack.
        6. Make new node a child of node in tree.
        """
        root_token = Root()
        scope_stack = [root_token]
        for token in self.stream:
            # print('Stack:::{}'.format(scope_stack))
            if token:
                parent = scope_stack[-1]
                if token.type == TOKEN_BLOCK_END:
                    #parent.exit_scope()
                    scope_stack.pop()
                    continue                        # We don't create Nodes for End Tokens!
                node = self.create_node(token)
                if node:
                    parent.children.append(node)
                    print('Parent: {}'.format(parent))
                    print('\tChildren: {}'.format(parent.children))
                    if node.creates_scope:
                        scope_stack.append(node)
        return scope_stack

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
    print(parser.generate_parse_tree())

    #for token in parser.stream:
    #    parser.create_node(token)
