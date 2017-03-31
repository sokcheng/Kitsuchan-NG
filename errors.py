#!/usr/bin/env python3

class Error(Exception):
    """Generic Error."""
    pass

class InputError(Error):
    """Raise when a command receives invalid input.
    
    expression - The invalid input in question.
    message - A message for the error.
    """
    def __init__(self, expression=None, message=None):
        self.expression = str(expression)
        if isinstance(message, str):
            self.message = message
        else:
            self.message = "Invalid input: %s" % (self.expression)
    def __str__(self):
        return self.message

class ContextError(Error):
    """Raise when a command is called in the wrong context.
    This may randomly change at some point as the error handling matures.
    
    ctx - The context in question.
    """
    def __init__(self, ctx=None):
        self.ctx = ctx
        self.message = "Invalid context."
    def __str__(self):
        return self.message

class ZeroDataLengthError(Error):
    """Raise when a command executes and receives data of length 0.
    This is mainly to be used in conjunction with aiohttp.ClientSession.get(), which may return
    undesirable values.
    """
    def __init__(self):
        self.message = "Data length is 0."
    def __str__(self):
        return self.message

class UserPermissionsError(Error):
    """Raise when a command executes but the user does not have permission.
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class BotPermissionsError(Error):
    """Raise when the bot tries to do a thing, but fails.
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
