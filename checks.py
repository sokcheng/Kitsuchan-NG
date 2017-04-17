#!/usr/bin/env python3

"""Custom checks for the bot."""

def is_nsfw(ctx):
    """An NSFW check for the bot."""
    return "nsfw" in ctx.channel.name.lower()
