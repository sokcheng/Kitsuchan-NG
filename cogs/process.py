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

class Core:
    """discord.py cog containing functions that halt/restart the bot.
    
    bot - The parent discord.Client object for the cog.
    """

    @commands.command()
    @commands.is_owner()
    async def halt(self, ctx):
        """Halt the bot. Must be bot owner to execute."""
        confirm = await helpers.yes_no(ctx, ctx.bot)
        if not confirm:
            return
        message = "Bot is going for halt NOW!"
        logger.warning(message)
        await ctx.send(message)
        await ctx.bot.logout()
        settings.save()
        ctx.bot.session.close()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot. Must be bot owner to execute."""
        confirm = await helpers.yes_no(ctx, ctx.bot)
        if not confirm:
            return
        message = "Bot is going for restart NOW!"
        logger.warning(message)
        await ctx.send(message)
        await ctx.bot.logout()
        ctx.bot.session.close()
        settings.save()
        os.execv(sys.executable, [sys.executable] + sys.argv)

def setup(bot):
    """Setup function for process."""
    bot.add_cog(Core())
