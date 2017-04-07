#!/usr/bin/env python3

"""This module contains checks that could be used in various places around the bot.

This module is currently largely obsolete. Where possible, one should use discord.py builtins."""

from __main__ import bot

def is_bot_owner(ctx):
    """Check whether the sender of a message is marked as the bot's owner."""
    if ctx.author.id == bot.owner.id:
        return True
    return False

def is_channel_admin(ctx):
    """Check whether the sender of a message could conceivably be an admin.""" 
    if ctx.guild is None:
        return False
    permissions_author = ctx.channel.permissions_for(ctx.author)
    if (permissions_author.manage_channels and permissions_author.manage_guild) is True \
    or ctx.author.id == ctx.guild.owner.id:
        return True
    return False
