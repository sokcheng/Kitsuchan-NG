#!/usr/bin/env python3

class Error(Exception):
    """Generic Error."""
    pass

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

class KeyError(Error):
    """Raise when an API key is not specified.
    """
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
