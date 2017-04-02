#!/usr/bin/env python3

"""Contains a cog with the bot's utility commands."""

# Standard modules
import sys
import datetime
import logging

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
from app_info import *
import settings
import errors
import utils

logger = logging.getLogger(__name__)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Utilities(bot, logger))

class Utilities:
    """discord.py cog containing utility functions of the bot.
    
    bot - The parent discord.Client object for the cog.
    logger - A logger to assign the cog.
    """
    
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

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
        settings.manager.setdefault("WHITELIST_NSFW", [])
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
    
    @commands.command(brief="Display a user's avatar.")
    async def avatar(self, ctx):
        """Display your avatar. Mention a user to display their's."""
        self.logger.info("Displaying user avatar.")
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.author
        name = user.name
        url = user.avatar_url
        embed = discord.Embed(title="The avatar of %s" % (name,))
        embed.url = url
        embed.set_image(url=url)
        await ctx.send(embed=embed)