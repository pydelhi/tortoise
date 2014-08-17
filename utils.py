#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast


class ContextError(Exception):
    pass


def resolve(token, context):
    """
    A context is a dict with keys and values. We resolve the values
    in the context based on their type.
    For example, for a variable {{ foo }} to be resolveld, the template has
    to be passed in the variable as context in its render function, like so:
        `myTemplate.render("template.html", context={'foo': 10})`
    or as Flask does it using kwargs:
        `myTemplate.render("template.html", foo=10)`
    """
    if '.' in token:
        t_split = token.split('.')
        rv = context.get(t_split[0], None)
        if rv and t_split[1:]:
            for i in t_split[1:]:
                try:
                    rv = getattr(rv, str(i))
                except AttributeError:
                    rv = rv[str(i)]
                if callable(rv):
                    rv = rv()
        return rv
    else:
        rv = context.get(token, None)
        if rv is None:
            raise ContextError('Context lookup failed!')
        return rv


def eval_expression(expr):
    try:
        return 'literal', ast.literal_eval(expr)
    except ValueError or IndentationError or SyntaxError:
        return 'name', expr
