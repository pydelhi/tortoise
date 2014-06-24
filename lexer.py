#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A Lexer for our templates!

"""
Example Syntax
--------------
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <p>Hello, {{ name }}!</p>
    {% for i in list %}
        <div class="foobar"> {{ i }}</div>
    {% endfor %}
</body>
</html>
"""

import re

import syntax

# For Lexical Analysis, we define Tokens for our language
TOKEN_DLBRACE = 'double_left_brace'
TOKEN_DRBRACE = 'double_right_brace'
TOKEN_BEGIN_SCOPE = 'scope_begin'
TOKEN_END_SCOPE = 'scope_end'
TOKEN_COMMENT_BEGIN = 'comment_begin'
TOKEN_COMMENT_END = 'comment_end'
TOKEN_BEGIN_COMMENT = 'comment_begin'
TOKEN_END_COMMENT = 'comment_end'
TOKEN_WHITESPACE = 'whitespace'
TOKEN_HTML = 'html'
TOKEN_EOF = 'eof'
TOKEN_TEMPLATE_VAR = 'template_variable'

TOKEN_DICT = {
        '{{': TOKEN_DLBRACE,
        '}}': TOKEN_DRBRACE,
        '{%': TOKEN_BEGIN_SCOPE,
        '%}': TOKEN_END_SCOPE,
        '{#': TOKEN_BEGIN_COMMENT,
        '#}': TOKEN_END_COMMENT,
}

c = lambda x: re.compile(x)
_RE_MEGA = c(r'({0}.*?{1})|({2}.*?{3})|({4}.*?{5})'.format(*syntax.SYMBOLS))

class LexerError(Exception):

    def __init__(self, line_no, col_no):
        self.line_no = line_no
        self.col_no = col_no


class Token(object):
    """
    Wrapper of each word Token seen in the source text.
    Along with the value of the token, some extra information is also
    stored as attributes.
    """

    def __init__(self, value, type, line_no=None, col_no=None):
        # Lets get this thing working first. Take care of line number, col number later!
        self.type = type
        self.value = value
        self.line_no = line_no
        self.col_no = col_no

    def __repr__(self):

        if self.value == ' ':
            value = '  SPACE'
        elif self.value == '\t':
            value = ' TAB'
        elif self.value == '\n':
            value = ' NEWLINE'
        elif self.value == '\0':
            value = ' EOF'
        else:
            value = self.value

        return '<<<Token {0} : {1} >>>'.format(self.type, value)


class Lexer(object):
    """A Regex based Lexer."""

    def __init__(self, source_text):
        self._source_text = source_text
        self._source_list = _RE_MEGA.split(self._source_text)
        self._pos = 0


    def __iter__(self):
        """
        Generator stream that returns the next token in our buffer.
        """
        if self._pos >= len(self._source_text):
            raise StopIteration
        else:
            for token in self._source_list:
                # Clean up a token and then return a proper Token object.
                # Symbol tokens are expected to be 2 char only!
                if token is not None:
                    token_set = ([token[:2], token[-2:]])
                    if token_set[0] in syntax.SYMBOLS and token_set[1] in syntax.SYMBOLS:
                        # Got a token pair with stuff inside. Split them up.
                        token_split_match = re.match(r'({0})\s*([\w\s]*)\s*({1})'.format(*token_set), token)

                        if token_split_match:
                            open_token_str = token_split_match.groups()[0]
                            open_token = Token(open_token_str, self.get_token_type(open_token_str))
                            close_token_str = token_split_match.groups()[-1]
                            close_token = Token(close_token_str, self.get_token_type(close_token_str))

                            # We can have multiple things inside a token-pair
                            # If it is not a keyword, it is most likely a variable.
                            # {% for item in list %} <some_html> {% endfor %}
                            # here, for...in are the keywords, and item and list are the variables.
                            # {{ }} token-pair can have variables as well as macros, but lets just stick
                            # to variables for now.

                            yield open_token

                            # Split up and yield everything inside the token-pair.
                            pair_scope_token_list = token[2:-2].split()
                            for raw_token in pair_scope_token_list:
                                yield Token(raw_token, self.get_token_type(raw_token))

                            yield close_token
                    else:
                        token_type = TOKEN_HTML
                        new_token = Token(token, token_type)
                        yield new_token


    def get_token_type(self, raw_token):
        """
        Classify tokens in their categories.
        """
        token_type = TOKEN_DICT.get(raw_token)
        if not token_type:
            if raw_token in syntax.KEYWORDS:
                # Keywords can be their own token
                token_type = raw_token
            else:
                token_type = TOKEN_TEMPLATE_VAR
        return token_type



if __name__ == '__main__':

    source = """
<h1>Hello, {{ name }}!!</h1>
<div class="some-class">
    {% for item in list %}
        <h2> {{ item }} </h2>
    {% endfor %}
</div>
"""
    lexer = Lexer(source)
    for i in lexer:
        print(i)
