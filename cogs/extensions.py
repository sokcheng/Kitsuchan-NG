#!/usr/bin/env python3

"""Contains a cog with the bot's extension commands."""

# Standard modules
import logging

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
import helpers
import settings

logger = logging.getLogger(__name__)

class Extensions:
    """Extension loading/unloading commands."""

    @commands.command(aliases=["loade"])
    @commands.is_owner()
    async def load(self, ctx, extension_name:str):
        """Enable the use of an extension.
        
        Only the bot owner can use this."""
        logger.info(f"Loading extension {extension_name}...")
        ctx.bot.load_extension(extension_name)
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        if extension_name not in settings.manager["EXTENSIONS"]:
            settings.manager["EXTENSIONS"].append(extension_name)
            message = f"Extension {extension_name} loaded."
        else:
            message = f"Extension {extension_name} is already loaded. :<"
        await ctx.send(message)
        logger.info(message)

    @commands.command(aliases=["reload", "rloade"])
    @commands.is_owner()
    async def rload(self, ctx, extension_name:str):
        """Reload an already-loaded extension.
        
        Only the bot owner can use this."""
        logger.info(f"Reloading extension {extension_name}...")
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        if extension_name in settings.manager["EXTENSIONS"]:
            ctx.bot.unload_extension(extension_name)
            try:
                ctx.bot.load_extension(extension_name)
            except Exception as error:
                message = f"An error occurred while trying to reload {extension_name}! x.x"
            else:
                message = f"Extension {extension_name} reloaded."
        else:
            message = f"Extension {extension_name} not currently loaded; please load it. :<"
        await ctx.send(message)
        logger.info(message)

    @commands.command(aliases=["unload", "uloade"])
    @commands.is_owner()
    async def uload(self, ctx, extension_name:str):
        """Disable the use of an extension.
        
        Only the bot owner can use this."""
        prompt = await helpers.yes_no(ctx, ctx.bot)
        if not prompt:
            return
        logger.info(f"Unloading extension {extension_name}...")
        ctx.bot.unload_extension(extension_name)
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        try:
            settings.manager["EXTENSIONS"].remove(extension_name)
        except ValueError:
            message = f"Extension {extension_name} is already unloaded. :<"
        else:
            message = f"Extension {extension_name} unloaded."
        await ctx.send(message)
        logger.info(message)

    @commands.command()
    @commands.is_owner()
    async def liste(self, ctx):
        """Display list of currently-enabled bot extensions.
        
        Only the bot owner can use this."""
        logger.info("Extension list requested.")
        extensions = "\n".join(ctx.bot.extensions)
        message = f"```Loaded extensions:\n{extensions}```"
        await ctx.author.send(message)
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Sent to DM!")

def setup(bot):
    """Setup function for Core."""
    bot.add_cog(Extensions())
