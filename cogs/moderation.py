#!/usr/bin/env python3

"""Contains a cog for moderation commands."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import settings
import checks
import helpers
import utils

logger = logging.getLogger(__name__)

def setup(bot):
    """Setup function for Moderation."""
    bot.add_cog(Moderation(bot))

class Moderation:
    """discord.py cog containing moderation functions of the bot.
    
    bot - The parent discord.Client object for the cog.
    logger - A logger to assign the cog.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(checks.is_channel_admin)
    async def kick(self, ctx):
        """Kick all users mentioned by this command."""
        await helpers.function_by_mentions(ctx, ctx.guild.kick)

    @commands.command()
    @commands.check(checks.is_channel_admin)
    async def ban(self, ctx):
        """Ban all users mentioned by this command."""
        await helpers.function_by_mentions(ctx, ctx.guild.ban)
        
    @commands.command()
    @commands.check(checks.is_channel_admin)
    async def purge(self, ctx, limit:int):
        """Purge a certain number of messages."""
        await ctx.channel.purge(limit=limit)

    @commands.command()
    @commands.check(checks.is_channel_admin)
    async def allownsfw(self, ctx, *, channel:discord.TextChannel=None):
        """Whitelists channel for NSFW content.
        Defaults to current channel. Channel ID is stored as an SHA-512 hash.
        
        channel - Optional. Mention a channel to change settings for that channel."""
        if not channel:
            channel = ctx.channel
        hash_id_channel = utils.to_hash(str(channel.id))
        settings.manager.setdefault("WHITELIST_NSFW", [])
        if hash_id_channel not in settings.manager["WHITELIST_NSFW"]:
            logger.info("NSFW content for %s is now enabled." % (ctx.channel.id,))
            settings.manager["WHITELIST_NSFW"].append(hash_id_channel)
            await ctx.send("NSFW content for this channel is now enabled.")
        else:
            await ctx.send("NSFW content is already enabled for this channel.")

    @commands.command()
    @commands.check(checks.is_channel_admin)
    async def denynsfw(self, ctx, *, channel:discord.TextChannel=None):
        """Blacklists channel for NSFW content.
        Defaults to current channel.
        
        channel - Optional. Mention a channel to change settings for that channel."""
        if not channel:
            channel = ctx.channel
        hash_id_channel = utils.to_hash(str(channel.id))
        settings.manager.setdefault("WHITELIST_NSFW", [])
        if hash_id_channel in settings.manager["WHITELIST_NSFW"]:
            logger.info("NSFW content for %s is now disabled." % (ctx.channel.id,))
            settings.manager["WHITELIST_NSFW"].remove(hash_id_channel)
            await ctx.send("NSFW content for this channel is now disabled.")
        else:
            await ctx.send("NSFW content is already disabled for this channel.")
