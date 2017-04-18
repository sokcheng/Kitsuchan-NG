#!/usr/bin/env python3

"""Contains a cog with the bot's invite command."""

# Standard library
import logging

# Third party modules
from discord.ext import commands

logger = logging.getLogger(__name__)

class Core:
    """discord.py cog containing core functions of the bot.
    
    * bot - The parent discord.Client object for the cog.
    """

    @commands.command()
    async def invite(self, ctx):
        """Generate an invite link for this bot."""
        logger.info(f"Invite requested by {ctx.author.name} ({ctx.author.id}).")
        message = f"https://discordapp.com/oauth2/authorize?client_id={ctx.bot.user.id}&scope=bot"
        await ctx.send(message)

def setup(bot):
    """Setup function for Invite."""
    bot.add_cog(Core())
