#!/usr/bin/env python3

"""Contains a cog with the bot's invite command."""

# Standard library
import logging

# Third party modules
from discord.ext import commands

logger = logging.getLogger(__name__)

class Invite:
    """Invite command."""

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def invite(self, ctx):
        """Generate an invite link for this bot."""
        message = f"https://discordapp.com/oauth2/authorize?client_id={ctx.bot.user.id}&scope=bot"
        await ctx.send(message)

def setup(bot):
    """Setup function for Invite."""
    bot.add_cog(Invite())
