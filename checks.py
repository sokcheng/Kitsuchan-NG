#!/usr/bin/env python3

"""Custom checks for the bot."""

def is_nsfw(ctx):
    """An NSFW check for the bot."""
    try:
        return "nsfw" in ctx.channel.name.lower()
    except AttributeError:
        return False
