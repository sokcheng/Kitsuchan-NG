#!/usr/bin/env python3

"""Contains a cog for moderation commands."""

# Third-party modules
import asyncio
import discord
from discord.ext import commands

# Bundled modules
from environment import *
import checks
import helpers

class Moderation:
    """discord.py cog containing core functions of the bot.
    
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
        
        Is NOT persistent. If the bot restarts, it won't remember this info."""
        if str(ctx.channel.id) not in WHITELIST_NSFW:
            self.logger.info("NSFW content for %s is now enabled." % (ctx.channel.id,))
            WHITELIST_NSFW.append(str(ctx.channel.id))
            await ctx.send("NSFW content for this channel is now enabled.")
        else:
            await ctx.send("NSFW content is already enabled for this channel.")

    @commands.command(brief="Blacklists channel for NSFW content.")
    @commands.check(checks.is_channel_admin)
    async def denynsfw(self, ctx):
        """Whitelists channel for NSFW content.
        
        Is NOT persistent. If the bot restarts, it won't remember this info."""
        if str(ctx.channel.id) in WHITELIST_NSFW:
            self.logger.info("NSFW content for %s is now disabled." % (ctx.channel.id,))
            WHITELIST_NSFW.remove(str(ctx.channel.id))
            await ctx.send("NSFW content for this channel is now disabled.")
        else:
            await ctx.send("NSFW content is already disabled for this channel.")
