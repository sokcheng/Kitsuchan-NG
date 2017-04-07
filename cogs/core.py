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
        # Split the message up by zero-width spaces so the bot doesn't trigger other bots.
        message = "\u200B"*2 + "\u200B".join(tuple(message))
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

    @commands.command(aliases=["load-extension"])
    @commands.check(checks.is_bot_owner)
    async def loade(self, ctx, extension_name:str):
        """Enable the use of an extension."""
        logger.info(f"Loading extension {extension_name}...")
        self.bot.load_extension(extension_name)
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        if extension_name not in settings.manager["EXTENSIONS"]:
            settings.manager["EXTENSIONS"].append(extension_name)
            message = f"Extension {extension_name} loaded"
        else:
            message = f"Extension {extension_name} is already loaded"
        await ctx.send(message)
        logger.info(message)

    @commands.command(aliases=["reload-extension"])
    @commands.check(checks.is_bot_owner)
    async def rloade(self, ctx, extension_name:str):
        """Reload an already-loaded extension."""
        logger.info(f"Reloading extension {extension_name}...")
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        if extension_name in settings.manager["EXTENSIONS"]:
            self.bot.unload_extension(extension_name)
            self.bot.load_extension(extension_name)
            message = f"Extension {extension_name} reloaded"
        else:
            message = f"Extension {extension_name} not currently loaded; please load it"
        await ctx.send(message)
        logger.info(message)

    @commands.command(aliases=["unload-extension"])
    @commands.check(checks.is_bot_owner)
    async def uloade(self, ctx, extension_name:str):
        """Disable the use of an extension."""
        prompt = await helpers.yes_no(ctx, self.bot)
        if not prompt:
            return
        logger.info(f"Unloading extension {extension_name}...")
        self.bot.unload_extension(extension_name)
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        try:
            settings.manager["EXTENSIONS"].remove(extension_name)
        except ValueError:
            message = f"Extension {extension_name} is already unloaded"
        else:
            message = f"Extension {extension_name} unloaded"
        await ctx.send(message)
        logger.info(message)

    @commands.command(aliases=["list-extensions"])
    @commands.check(checks.is_bot_owner)
    async def liste(self, ctx):
        """Display list of currently-enabled bot extensions."""
        logger.info("Extension list requested.")
        extensions = "\n".join(self.bot.extensions)
        message = f"```Loaded extensions:\n{extensions}```"
        await ctx.author.send(message)
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Sent to DM!")

def setup(bot):
    """Setup function for Core."""
    bot.add_cog(Core(bot))
