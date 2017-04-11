#!/usr/bin/env python3

"""Contains a cog for moderation commands."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import settings
import helpers
import utils

logger = logging.getLogger(__name__)

class Moderation:
    """discord.py cog containing moderation functions of the bot."""
    def __init__(self):
        pass

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx):
        """Kick all users mentioned by this command."""
        await helpers.function_by_mentions(ctx, ctx.guild.kick)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx):
        """Ban all users mentioned by this command."""
        await helpers.function_by_mentions(ctx, ctx.guild.ban)
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, limit:int):
        """Purge a certain number of messages."""
        await ctx.channel.purge(limit=limit)

def setup(bot):
    """Setup function for Moderation."""
    bot.add_cog(Moderation())
