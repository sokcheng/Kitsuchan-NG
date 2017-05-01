#!/usr/bin/env python3

"""Contains a cog that fetches discriminators."""

# Standard modules
import logging

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
import helpers

logger = logging.getLogger(__name__)

class Discriminator:
    """Discriminator command."""
    
    @commands.command(aliases=["discriminator"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def discrim(self, ctx, *, discriminator:str=None):
        """Find all users in the current guild with a given discriminator.
        
        * discriminator - A discriminator to search for."""
        if not discriminator:
            discriminator = str(ctx.author.discriminator)
        results = []
        for member in ctx.guild.members:
            if str(member.discriminator) == discriminator:
                results.append(f"[{len(results)+1}] {member.name}#{member.discriminator}")
        if len(results) == 0:
            await ctx.send("Could not find any members in this guild with that discriminator.")
            return
        paginator = commands.Paginator(prefix="```py")
        if len(results) > 1:
            plural = "s"
        else:
            plural = ""
        paginator.add_line(f"Found {len(results)} member{plural} of this guild ({discriminator}):")
        for member in results[:10]:
            paginator.add_line(member)
        if len(results) > 10:
            paginator.add_line(f"...and {len(results)-10} others.")
        for page in paginator.pages:
            await ctx.send(page)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Discriminator())
