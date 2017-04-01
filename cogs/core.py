#!/usr/bin/env python3

"""Contains a cog with the bot's core commands."""

# Standard modules
import sys
import os
import logging

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
from __main__ import __file__ as FILE_MAIN # This sucks
import checks
import settings
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
        self.bot = bot
        self.logger = logger
    
    @commands.command(brief="Repeat the user's text back at them.", aliases=["say"])
    async def echo(self, ctx, *text):
        """Repeat the user's text back at them.
        
        *text - A list of strings, which is concatenated into one string before being echoed.
        """
        await ctx.send(" ".join(text))
    
    @commands.command(brief="Halt the self.bot.", aliases=["h"])
    @commands.check(checks.is_bot_owner)
    async def halt(self, ctx):
        """Halt the self.bot. Must be bot owner to execute."""
        self.logger.warning("Halting bot!")
        await ctx.send("Halting.")
        await self.bot.logout()
        settings.save()
        self.bot.session.close()

    @commands.command(brief="Restart the self.bot.", aliases=["r"])
    @commands.check(checks.is_bot_owner)
    async def restart(self, ctx):
        """Restart the self.bot. Must be bot owner to execute."""
        self.logger.warning("Restarting bot!")
        await ctx.send("Restarting.")
        await self.bot.logout()
        self.bot.session.close()
        settings.save()
        os.execl(os.path.realpath(FILE_MAIN), *sys.argv)
