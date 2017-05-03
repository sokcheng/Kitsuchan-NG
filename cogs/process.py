#!/usr/bin/env python3

# Standard modules
import sys
import os
import logging
import subprocess

# Third party modules
from discord.ext import commands

# Bundled modules
from __main__ import __file__ as FILE_MAIN # This sucks
import helpers
import settings

logger = logging.getLogger(__name__)

class Process:
    """Commands that affect the bot's running process."""

    @commands.command(aliases=["shutdown", "kys"])
    @commands.is_owner()
    async def halt(self, ctx):
        """Halt the bot. Only the bot owner can use this."""
        confirm = await helpers.yes_no(ctx, ctx.bot)
        if not confirm:
            return
        if ctx.invoked_with == "kys":
            message = "Dead! x.x"
        else:
            message = "Bot is going for halt NOW!"
        logger.warning(message)
        await ctx.send(message)
        await ctx.bot.logout()
        settings.save()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot. Only the bot owner can use this."""
        confirm = await helpers.yes_no(ctx, ctx.bot)
        if not confirm:
            return
        message = "Bot is going for restart NOW!"
        logger.warning(message)
        await ctx.send(message)
        await ctx.bot.logout()
        settings.save()
        os.execv(sys.executable, [sys.executable] + sys.argv)

def setup(bot):
    """Setup function for process."""
    bot.add_cog(Process())
