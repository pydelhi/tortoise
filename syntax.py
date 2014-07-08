#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

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

VARIABLE_STARTCHARS = string.letters
VARIABLE_CHARS = string.letters + string.digits + '_'
WHITESPACE_CHARS = " \n\t"
STRING_CHARS = '"' + "'"
BLOCKNAME_CHARS = string.letters
