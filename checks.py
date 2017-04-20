#!/usr/bin/env python3

"""Custom checks for the bot."""

# Third-party libraries
from discord.ext import commands

# Bundled modules
import errors

NSFW_DISALLOWED = "NSFW disallowed for this context."

def is_nsfw(ctx):
    """An NSFW check for the bot."""
    try:
        allowed = "nsfw" in ctx.channel.name.lower()
        if allowed:
            return True
        raise errors.NSFWDisallowed(NSFW_DISALLOWED)
    except AttributeError:
        raise errors.NSFWDisallowed(NSFW_DISALLOWED)
