#!/usr/bin/env python3

"""Contains a cog with commands that handle NSFW togglling."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import settings
import checks
import utils

logger = logging.getLogger(__name__)

class Moderation:
    """discord.py cog containing commands that handle the NSFW whitelist."""
    def __init__(self):
        pass

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
            logger.info(f"NSFW content for {ctx.channel.id} is now enabled.")
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
            logger.info(f"NSFW content for {ctx.channel.id} is now disabled.")
            settings.manager["WHITELIST_NSFW"].remove(hash_id_channel)
            await ctx.send("NSFW content for this channel is now disabled.")
        else:
            await ctx.send("NSFW content is already disabled for this channel.")

def setup(bot):
    """Setup function for Moderation."""
    bot.add_cog(Moderation())