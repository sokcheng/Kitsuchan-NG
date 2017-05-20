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
        """Find all users the bot can see with a given discriminator.
        
        * discriminator - (optional) A discriminator to search for."""
        if not discriminator:
            discriminator = str(ctx.author.discriminator)
        results = []
        for user in ctx.bot.users:
            if str(user.discriminator) == discriminator:
                results.append(f"{len(results)+1}. {user.name}#{user.discriminator}")
        if len(results) == 0:
            await ctx.send(f"I couldn't find anyone with that discriminator. :<")
            return
        paginator = commands.Paginator(prefix="```markdown")
        if len(results) > 1:
            plural_users = "s"
        else:
            plural_users = ""
        if len(ctx.bot.guilds) > 1:
            plural_guilds = "s"
        else:
            plural_guilds = ""
        paginator.add_line((f"# Found {len(results)} user{plural_users} across "
                            f"{len(ctx.bot.guilds)} guild{plural_guilds} ({discriminator}) #"))
        for member in results[:10]:
            paginator.add_line(member)
        if len(results) > 10:
            paginator.add_line(f"...and {len(results)-10} others.")
        for page in paginator.pages:
            await ctx.send(page)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Discriminator())
