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

STATUS_INDICATORS = {"online": ":green_heart:",
                     "idle": ":yellow_heart:",
                     "dnd": ":heart:",
                     "offline": ":black_heart:"}
STATUS_SORTED = list(STATUS_INDICATORS.keys())

class Moderation:
    """discord.py cog containing moderation functions of the bot."""
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def kick(self, ctx):
        """Kick all users mentioned by this command.
        
        Requires both the user and bot to have `kick_members` to execute.
        """
        await helpers.function_by_mentions(ctx, ctx.guild.kick)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def ban(self, ctx):
        """Ban all users mentioned by this command.
        
        Requires both the user and bot to have `ban_members` to execute.
        """
        await helpers.function_by_mentions(ctx, ctx.guild.ban)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def unban(self, ctx):
        """Unban all users mentioned by this command.
        
        Requires both the user and bot to have `ban_members` to execute.
        """
        await helpers.function_by_mentions(ctx, ctx.guild.unban)

    @commands.command(aliases=["prune"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def purge(self, ctx, limit:int):
        """Purge a certain number of messages from the channel.
        
        Requires both the user and bot to have `manage_messages` to execute.
        """
        await ctx.channel.purge(limit=limit)

    def _sort_by_status(self, status):
        if status in STATUS_SORTED:
            return STATUS_SORTED.index(status)
        return 10

    @commands.command(aliases=["moderators"])
    @commands.cooldown(1, 12, commands.BucketType.channel)
    async def mods(self, ctx):
        """Display moderators for the given channel.
        
        Assumes that members with `manage_messages`, `kick_members`, and `ban_members` are mods.
        """
        the_mods = []
        for member in ctx.guild.members:
            if ctx.channel.permissions_for(member).manage_messages \
            and ctx.channel.permissions_for(member).kick_members \
            and ctx.channel.permissions_for(member).ban_members \
            and not member.bot:
                the_mods.append(member)
        the_mods.sort(key=lambda mod: self._sort_by_status(mod.status.name))
        message = ["**__Moderators__**"]
        for mod in the_mods:
            try:
                status = STATUS_INDICATORS[mod.status.name]
            except KeyError:
                status = STATUS_INDICATORS["offline"]
            message.append(f"{status} **{mod.name}**#{mod.discriminator}")
        message = "\n".join(message)
        await ctx.send(message)

def setup(bot):
    """Setup function for Moderation."""
    bot.add_cog(Moderation())
