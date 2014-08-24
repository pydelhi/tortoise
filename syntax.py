#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import operator

KEYWORDS = """
block
extends
for
endfor
if
else
endif
in
""".split()

SYMBOLS = """
{{
}}
{%
%}
{#
#}
""".split()

OP_TABLE = {
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne
}

VARIABLE_STARTCHARS = string.letters
VARIABLE_CHARS = string.letters + string.digits + '_'
WHITESPACE_CHARS = " \n\t"
STRING_CHARS = '"' + "'"
BLOCKNAME_CHARS = string.letters
