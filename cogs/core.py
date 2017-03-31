#!/usr/bin/env python3

"""Contains a cog with the bot's core commands."""

# Standard modules
import sys
import os
import datetime
import logging

# Third party modules
import asyncio
import discord
from discord.ext import commands

# Bundled modules
from __main__ import __file__ as FILE_MAIN # This sucks
from app_info import *
import settings
import errors
import utils

logger = logging.getLogger(__name__)

def setup(bot):
    """Setup function for Core."""
    bot.add_cog(Core(bot, logger))

class Core:
    """discord.py cog containing core functions of the bot.
    
    bot - The parent discord.Client object for the cog.
    logger - A logger to assign the cog.
    """
    
    def __init__(self, bot, logger):
        self.name = "Core Functions"
        self.bot = bot
        self.logger = logger
    
    def is_bot_owner(self, ctx):
        """Check whether the sender of a message is marked as the bot's owner."""
        if ctx.author.id == self.bot.owner.id:
            return True
        return False

    @commands.command(brief="Display bot information.", aliases=["info"])
    async def about(self, ctx):
        """Display information about this bot, such as library versions."""
        self.logger.info("Displaying info about me.")
        uptime = str(datetime.datetime.now() - self.bot.time_started).split(".")[0]
        embed = discord.Embed(title=APP_NAME)
        embed.url = APP_URL
        embed.description = self.bot.description
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Version", value=APP_VERSION_STRING)
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Python", value="%s.%s.%s" % sys.version_info[:3])
        embed.add_field(name="discord.py", value=discord.__version__)
        await ctx.send(embed=embed)

    @commands.command(brief="Display guild information.", aliases=["ginfo"])
    async def guildinfo(self, ctx):
        """Display information about the current guild, such as owner, region, emojis, and roles."""
        self.logger.info("Displaying info about guild.")
        guild = ctx.guild
        if guild is None:
            raise errors.ContextError("Not in a guild.")
        embed = discord.Embed(title=guild.name)
        embed.description = str(guild.id)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Owner", value=guild.owner.name)
        embed.add_field(name="Members", value=str(guild.member_count))
        count_channels = str(len(tuple(0 for x in guild.channels if isinstance(x, discord.TextChannel))))
        embed.add_field(name="Text channels", value=count_channels)
        count_channels_voice = str(len(tuple(0 for x in guild.channels if isinstance(x, discord.VoiceChannel))))
        embed.add_field(name="Voice channels", value=count_channels_voice)
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Created at", value=guild.created_at.ctime())
        emojis = ", ".join((emoji.name for emoji in guild.emojis))
        if len(emojis) > 0:
            embed.add_field(name="Custom emojis", value=emojis)
        roles = ", ".join((role.name for role in guild.roles))
        embed.add_field(name="Roles", value=roles, inline=False)
        await ctx.send(embed=embed)

    @commands.command(brief="Display channel info.", aliases=["cinfo"])
    async def channelinfo(self, ctx):
        """Display information about the current channel."""
        self.logger.info("Displaying info about channel.")
        channel = ctx.channel
        if channel is None:
            raise errors.ContextError()
        embed = discord.Embed(title="#%s" % (channel.name,))
        try:
            embed.description = channel.topic
        except AttributeError:
            pass
        embed.add_field(name="Channel ID", value=str(channel.id))
        try:
            embed.add_field(name="Guild", value=channel.guild.name)
        except AttributeError:
            pass
        embed.add_field(name="Created at", value=channel.created_at.ctime())
        hash_id_channel = utils.to_hash(str(ctx.channel.id))
        if hash_id_channel in settings.manager["WHITELIST_NSFW"]:
            embed.set_footer(text="NSFW content is enabled for this channel.")
        await ctx.send(embed=embed)

    @commands.command(brief="Display user info.", aliases=["uinfo"])
    async def userinfo(self, ctx):
        """Display information about you, such as status and roles.
        
        Mention a user while invoking this command to display information about that user."""
        self.logger.info("Displaying info about user.")
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.author
        embed = discord.Embed(title=user.display_name)
        if user.display_name != user.name:
            embed.description = user.name
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="User ID", value=str(user.id))
        if user.bot:
            embed.add_field(name="Bot?", value="Yes")
        status = str(user.status).capitalize()
        if status == "Dnd":
            status = "Do Not Disturb"
        embed.add_field(name="Status", value=status)
        if user.game:
            embed.add_field(name="Playing", value=user.game.name)
        embed.add_field(name="Joined guild at", value=user.joined_at.ctime())
        embed.add_field(name="Joined Discord at", value=user.created_at.ctime())
        roles = ", ".join((str(role) for role in user.roles))
        embed.add_field(name="Roles", value=roles, inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(brief="Repeat the user's text back at them.", aliases=["say"])
    async def echo(self, ctx, *text):
        """Repeat the user's text back at them.
        
        *text - A list of strings, which is concatenated into one string before being echoed.
        """
        await ctx.send(" ".join(text))
    
    @commands.command(brief="Halt the self.bot.", aliases=["h"])
    async def halt(self, ctx):
        """Halt the self.bot. Must be bot owner to execute."""
        if not self.is_bot_owner(ctx):
            message = "%s does not have permission." % str(ctx.author.id)
            await ctx.send(message)
            raise errors.UserPermissionsError(message)
        self.logger.warning("Halting bot!")
        await ctx.send("Halting.")
        await self.bot.logout()
        settings.save()
        self.bot.session.close()

    @commands.command(brief="Restart the self.bot.", aliases=["r"])
    async def restart(self, ctx):
        """Restart the self.bot. Must be bot owner to execute."""
        if not self.is_bot_owner(ctx):
            message = "%s does not have permission." % str(ctx.author.id)
            await ctx.send(message)
            raise errors.UserPermissionsError(message)
        self.logger.warning("Restarting bot!")
        await ctx.send("Restarting.")
        await self.bot.logout()
        self.bot.session.close()
        settings.save()
        os.execl(os.path.realpath(FILE_MAIN), *sys.argv)
