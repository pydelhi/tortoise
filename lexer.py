#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A Lexer for our templates!

import re
from collections import deque

import syntax
from tokens import *
from exc import TemplateSyntaxError

c = lambda x: re.compile(x)
_RE_MEGA = c(r'({0}.*?{1})|({2}.*?{3})|({4}.*?{5})'.format(*syntax.SYMBOLS))

class SyntaxError(Exception):

    def __init__(self, line_no, col_no):
        self.line_no = line_no
        self.col_no = col_no


class Token(object):
    """
    Wrapper of each word Token seen in the source text.
    Along with the value of the token, some extra information is also
    stored as attributes.
    """

    def __init__(self, value, line_no=None, col_no=None):
        # Lets get this thing working first. Take care of line number, col number later!
        self.value = value
        self.line_no = line_no
        self.col_no = col_no
        self.type = self.get_token_type()


    def get_token_type(self):
        """
        Analyse the token content and return the token type.
        """
        token_begin = self.value[:2]
        token_end = self.value[-2:]
        token_set = (token_begin, token_end)
        if token_set[0] in syntax.SYMBOLS and token_set[1] in syntax.SYMBOLS:
            token_content = self.value[2:-2].strip()
            if token_content[:3] == 'end':
                token_type = TOKEN_BLOCK_END
            else:
                token_type = TOKEN_DICT.get(token_begin)
            self.check_token_syntax(token_type, token_content)
        else:
            token_type = TOKEN_HTML
        return token_type

    def clean(self):
        if self.type in [TOKEN_VAR, TOKEN_BLOCK]:
            return ''.join(self.value[2:-2])
        return self.value

    def check_token_syntax(self, token_type, token_content):
        """
        Some basic syntax analysis here, based on token types.
        """
        if token_type == TOKEN_BLOCK_END and len(token_content.split()) > 1:
            raise TemplateSyntaxError('Invalid end token!')
        elif token_type == TOKEN_BLOCK:
            split = token_content.split()
            if split[0] not in syntax.KEYWORDS:
                raise TemplateSyntaxError('Invalid keyword - {0}'.format(split[0]))

    def __repr__(self):
        return '[Token] {0} -- {1}'.format(self.type, self.value)


class Lexer(object):
    """A Regex based Lexer."""

    def __init__(self, source_text):
        self._source_text = source_text.strip()
        self._source_list = [e for e in re.split(_RE_MEGA, self._source_text) if e]
        self._pos = 0
        self.current = TOKEN_INITIAL
        self._buffer = deque()

    def push(self, item):
        self._buffer.append(item)

    def peek(self):
        """
        Look ahead in the current stream,
        and return the next token. This does not
        affect the stream iterator.
        """
        pass

    def __iter__(self):
        """
        Generator stream that returns the next token in our buffer.
        """
        #if self._pos >= len(self._source_text):
        #    raise StopIteration
        #else:
        # print(self._source_list)
        # import pdb; pdb.set_trace()
        for text in self._source_list:
            self.current = Token(text)
            yield self.current




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
    lexer = Lexer(source)
    for i in lexer:
        print(i)
