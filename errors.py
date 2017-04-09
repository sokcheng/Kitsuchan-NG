#!/usr/bin/env python3

class Error(Exception):
    """Generic Error class for Kitsuchan-NG errors."""
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
    data that just straight up has length 0.
    """
    def __init__(self):
        self.message = "Data length is 0."
    def __str__(self):
        return self.message

class KeyError(Error):
    """Raise when a command executes, but needs an API key that was not specified.
    
    message - The message associated with the command."""
    def __init__(self, message:str=None):
        if message:
            self.message = message
        else:
            self.message = ("This command needs an API key, but one was not specified in the"
                            "configuration files.")
    def __str__(self):
        return self.message
