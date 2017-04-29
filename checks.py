#!/usr/bin/env python3

"""Custom checks for the bot."""

# Third-party libraries
from discord.ext import commands

# Bundled modules
import errors

NSFW_DISALLOWED = "NSFW disallowed for this context."

def is_nsfw(ctx):
    """An NSFW check for the bot."""
    if hasattr(ctx.channel, "is_nsfw") and ctx.channel.is_nsfw():
        return True
    raise errors.NSFWDisallowed(NSFW_DISALLOWED)
