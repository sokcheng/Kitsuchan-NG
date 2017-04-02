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
    bot.add_cog(Moderation(bot, logger))

class Moderation:
    """discord.py cog containing moderation functions of the bot.
    
    bot - The parent discord.Client object for the cog.
    logger - A logger to assign the cog.
    """
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.command(brief="Kick all users mentioned by this command.")
    @commands.check(checks.is_channel_admin)
    async def kick(self, ctx):
        """Kick all users mentioned by this command."""
        await helpers.function_by_mentions(ctx, self.bot.http.kick, True, ctx.guild.id)

    @commands.command(brief="Ban all users mentioned by this command.")
    @commands.check(checks.is_channel_admin)
    async def ban(self, ctx):
        """Ban all users mentioned by this command."""
        await helpers.function_by_mentions(ctx, self.bot.http.ban, True, ctx.guild.id)

    @commands.command(brief="Whitelists channel for NSFW content.")
    @commands.check(checks.is_channel_admin)
    async def allownsfw(self, ctx):
        """Whitelists channel for NSFW content.
        
        Persistent! Channel ID is stored as an SHA-512 hash."""
        hash_id_channel = utils.to_hash(str(ctx.channel.id))
        settings.manager.setdefault("WHITELIST_NSFW", [])
        if hash_id_channel not in settings.manager["WHITELIST_NSFW"]:
            self.logger.info("NSFW content for %s is now enabled." % (ctx.channel.id,))
            settings.manager["WHITELIST_NSFW"].append(hash_id_channel)
            await ctx.send("NSFW content for this channel is now enabled.")
        else:
            await ctx.send("NSFW content is already enabled for this channel.")

    @commands.command(brief="Blacklists channel for NSFW content.")
    @commands.check(checks.is_channel_admin)
    async def denynsfw(self, ctx):
        """Blacklists channel for NSFW content.
        
        Persistent!"""
        hash_id_channel = utils.to_hash(str(ctx.channel.id))
        settings.manager.setdefault("WHITELIST_NSFW", [])
        if hash_id_channel in settings.manager["WHITELIST_NSFW"]:
            self.logger.info("NSFW content for %s is now disabled." % (ctx.channel.id,))
            settings.manager["WHITELIST_NSFW"].remove(hash_id_channel)
            await ctx.send("NSFW content for this channel is now disabled.")
        else:
            await ctx.send("NSFW content is already disabled for this channel.")
