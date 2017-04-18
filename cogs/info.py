#!/usr/bin/env python3

# Standard modules
import datetime
import logging
import sys

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
import app_info
import errors
import helpers
import settings

logger = logging.getLogger(__name__)

class Utilities:
    """discord.py cog containing info commands, such as server and user info."""

    @commands.group(aliases=["a", "info", "i"], invoke_without_command=True)
    async def about(self, ctx):
        """Information subcommands, e.g. channel information."""
        embed = helpers.generate_help_embed(self.about)
        await ctx.send(embed=embed)

    @about.command(name="bot")
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def _infobot(self, ctx):
        """Display bot info, e.g. library versions."""
        logger.info("Displaying info about the bot.")
        uptime = str(datetime.datetime.now() - ctx.bot.time_started).split(".")[0]
        embed = discord.Embed()
        embed.description = ctx.bot.description
        if ctx.guild and ctx.guild.explicit_content_filter.name == "disabled":
            embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        else:
            embed.set_footer(text="Thumbnail omitted on this guild due to image scanning.")
        ainfo = await ctx.bot.application_info()
        owner = ainfo.owner.mention
        embed.add_field(name="Version", value=app_info.VERSION_STRING)
        embed.add_field(name="Owner", value=owner)
        num_guilds = len(ctx.bot.guilds)
        num_users = len([0 for member in ctx.bot.get_all_members()])
        embed.add_field(name="Serving", value=f"{num_users} users in {num_guilds} guilds")
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Python", value="{0}.{1}.{2}".format(*sys.version_info))
        embed.add_field(name="discord.py", value=discord.__version__)
        try:
            cookies_eaten = sum(discord.version_info[:3]) * sum(app_info.VERSION[:3])
            embed.add_field(name="Cookies eaten", value=str(cookies_eaten))
        except Exception:
            pass
        await ctx.send(embed=embed)

    @about.command(brief="Display guild info.", aliases=["g", "server", "s"])
    @commands.guild_only()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def guild(self, ctx):
        """Display information about the current guild, such as owner, region, emojis, and roles."""
        logger.info("Displaying info about guild.")
        guild = ctx.guild
        embed = discord.Embed(title=guild.name)
        embed.description = str(guild.id)
        if ctx.guild.explicit_content_filter.name == "disabled":
            embed.set_thumbnail(url=guild.icon_url)
        else:
            embed.set_footer(text="Thumbnail omitted on this guild due to image scanning.")
        embed.add_field(name="Owner", value=guild.owner.name)
        embed.add_field(name="Members", value=str(guild.member_count))
        count_channels = str(len(tuple(0 for x in guild.channels if isinstance(x, discord.TextChannel))))
        embed.add_field(name="Text channels", value=count_channels)
        count_channels_voice = str(len(tuple(0 for x in guild.channels if isinstance(x, discord.VoiceChannel))))
        embed.add_field(name="Voice channels", value=count_channels_voice)
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Created at", value=guild.created_at.ctime())
        # 1024 to respect embed limits
        emojis = ", ".join((emoji.name for emoji in guild.emojis))[:1024]
        if len(emojis) > 0:
            embed.add_field(name="Custom emojis", value=emojis)
        roles = ", ".join((role.name for role in guild.roles))[:1024]
        embed.add_field(name="Roles", value=roles, inline=False)
        await ctx.send(embed=embed)

    @about.command(brief="Display channel info.", aliases=["c"])
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def channel(self, ctx, channel:discord.TextChannel=None):
        """Display information about a channel channel.
        Defaults to the current channel.
        
        * channel - Optional argument. A specific channel to get information about."""
        logger.info("Displaying info about channel.")
        if not channel:
            channel = ctx.channel
        embed = discord.Embed(title=f"{channel.name}")
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
        await ctx.send(embed=embed)

    @about.command(brief="Display user info.", aliases=["u"])
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def user(self, ctx, user:discord.Member=None):
        """Display information about a user, such as status and roles.
        Defaults to the user who invoked the command.
        
        * user - Optional argument. A user in the current channel to get user information about."""
        logger.info("Displaying info about user.")
        if not user:
            user = ctx.author
        embed = discord.Embed(title=user.display_name)
        if user.display_name != user.name:
            embed.description = user.name
        if ctx.guild and ctx.guild.explicit_content_filter.name == "disabled":
            embed.set_thumbnail(url=user.avatar_url)
        else:
            embed.set_footer(text="Thumbnail omitted on this guild due to image scanning.")
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
        roles = ", ".join((str(role) for role in user.roles))[:1024]
        embed.add_field(name="Roles", value=roles, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Utilities())
