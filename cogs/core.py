#!/usr/bin/env python3

"""Contains a cog with the bot's core commands."""

# Standard modules
import sys
import os
import datetime
import logging

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
from __main__ import __file__ as FILE_MAIN # This sucks
import app_info
import checks
import helpers
import settings
import utils

logger = logging.getLogger(__name__)

def setup(bot):
    """Setup function for Core."""
    bot.add_cog(Core(bot))

class Core:
    """discord.py cog containing core functions of the bot.
    
    bot - The parent discord.Client object for the cog.
    logger - A logger to assign the cog.
    """
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        """Display information about this bot, such as library versions."""
        logger.info("Displaying info about the bot.")
        uptime = str(datetime.datetime.now() - self.bot.time_started).split(".")[0]
        embed = discord.Embed()
        embed.description = self.bot.description
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        ainfo = await self.bot.application_info()
        owner = ainfo.owner.mention
        embed.add_field(name="Version", value=app_info.VERSION_STRING)
        embed.add_field(name="Owner", value=owner)
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Python", value="%s.%s.%s" % sys.version_info[:3])
        embed.add_field(name="discord.py", value=discord.__version__)
        try:
            cookies_eaten = sum(discord.version_info[:3]) * sum(app_info.VERSION[:3])
        except Exception:
            cookies_eaten = 4
        embed.add_field(name="Cookies eaten", value=str(cookies_eaten))
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["say"])
    async def echo(self, ctx, *text):
        """Repeat the user's text back at them.
        
        *text - A list of strings, which is concatenated into one string before being echoed.
        """
        message = " ".join(text)
        if len(message) == 0:
            message = "Echo?"
        message = "\u200B" + message
        await ctx.send(message)
    
    @commands.command()
    @commands.check(checks.is_bot_owner)
    async def halt(self, ctx):
        """Halt the bot. Must be bot owner to execute."""
        confirm = await helpers.yes_no(ctx, self.bot)
        if not confirm:
            return
        logger.warning("Bot is going for HALT now!")
        embed = discord.Embed(title="Halting.", color=discord.Color.red())
        await ctx.send(embed=embed)
        await self.bot.logout()
        settings.save()
        self.bot.session.close()

    @commands.command()
    @commands.check(checks.is_bot_owner)
    async def restart(self, ctx):
        """Restart the bot. Must be bot owner to execute."""
        confirm = await helpers.yes_no(ctx, self.bot)
        if not confirm:
            return
        logger.warning("Bot is going for RESTART now!")
        embed = discord.Embed(title="Restarting.", color=discord.Color.red())
        await ctx.send(embed=embed)
        await self.bot.logout()
        self.bot.session.close()
        settings.save()
        os.execl(os.path.realpath(FILE_MAIN), *sys.argv)
