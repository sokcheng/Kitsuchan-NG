#!/usr/bin/env python3

class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, expression=None, message=None):
        self.expression = str(expression)
        if isinstance(message, str):
            self.message = message
        else:
            self.message = "Invalid input: %s" % (self.expression)
    def __str__(self):
        return self.message

class ContextError(Error):
    def __init__(self, ctx=None):
        self.ctx = ctx
        self.message = "Invalid context."
    def __str__(self):
        return self.message
