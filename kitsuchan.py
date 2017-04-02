#!/usr/bin/env python3

"""Retrieve anime images and do other stuff with a Discord bot.

This is free and unencumbered software released into the public domain, under the Creative Commons
CC0 1.0 Universal Public Domain Dedication.

URL to legal text: https://creativecommons.org/publicdomain/zero/1.0/legalcode
"""

# Standard modules
import sys
import datetime
import logging

# Third-party modules
import aiohttp
import discord
from discord.ext import commands

# Bundled modules
from app_info import *
import settings

assert (sys.version_info >= (3,5)), "This program requires Python 3.5 or higher."
assert (discord.version_info >= (1,0)), "This program requires Discord 1.0 or higher."

# Initialization

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = commands.Bot(command_prefix="kit!", pm_help=True)
bot.description = APP_DESCRIPTION
bot.session = aiohttp.ClientSession(loop=bot.loop)

# Checking functions

@bot.check
def is_human(ctx):
    """Check whether the sender of a message is a human or a bot."""
    return not ctx.author.bot

# Events

@bot.event
async def on_ready():
    """Conduct preparations once the bot is ready to go."""
    bot.time_started = datetime.datetime.now()
    command_prefix = settings.manager.get("COMMAND_PREFIX")
    if isinstance(command_prefix, str):
        bot.command_prefix = command_prefix
    else:
        bot.command_prefix = bot.user.name[:3].lower() + "!"
    ainfo = await bot.application_info()
    bot.owner = ainfo.owner
    game = discord.Game()
    game.name = bot.command_prefix + "help"
    await bot.change_presence(game=game)
    logger.info("Bot is ONLINE! Username: %s, User ID: %s", bot.user.name, bot.user.id)

@bot.event
async def on_command_completion(ctx):
    """Trigger when a command completes successfully."""
    if ctx.invoked_with == "help":
        await ctx.send("Help sent to DM.")

@bot.event
async def on_command_error(exception, ctx):
    """Handle errors that occur in commands."""
    if isinstance(exception, commands.CheckFailure):
        await ctx.send("Permission denied!")
        logger.info("%s (%s) tried to issue a command but was denied." % (ctx.author.name,
                                                                          ctx.author.id))
    elif isinstance(exception, (discord.HTTPException, commands.MissingRequiredArgument)):
        await ctx.send(str(exception))
        logger.info(exception)
    else:
        logger.info(exception)

def main():
    """It's the main function. You call this to start the bot."""
    try:
        settings.manager["OAUTH_TOKEN_DISCORD"]
    except KeyError:
        print("Please enter an OAuth token for this bot, so it can sign into Discord.")
        settings.manager["OAUTH_TOKEN_DISCORD"] = input("> ")
    logger.info("Warming up...")
    extensions = settings.manager.get("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
    for extension in extensions:
        logger.info("Loading extension %s", extension)
        try:
            bot.load_extension(extension)
            logger.info("Extension %s loaded", extension)
        except Exception as error:
            logger.warning("Extension %s seems to be broken", extension)
            logger.warning(error)
    bot.run(settings.manager["OAUTH_TOKEN_DISCORD"])

if __name__ == "__main__":
    main()
