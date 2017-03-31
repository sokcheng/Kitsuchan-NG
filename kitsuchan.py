#!/usr/bin/env python3

"""Retrieve anime images with a Discord bot.

This is free and unencumbered software released into the public domain, under the Creative Commons
CC0 1.0 Universal Public Domain Dedication.

URL to legal text: https://creativecommons.org/publicdomain/zero/1.0/legalcode

Usage::

Required environment variables:
* API_KEY_DISCORD - OAuth token for Discord.
* API_KEY_IBSEARCH - API key for IbSear.ch.

Optional environment variables:
* COMMAND_PREFIX - Override the bot's command prefix.
* WHITELIST_NSFW - List of channels to allow NSFW content on.
"""

# Standard modules
import os
import json
import logging
import random
import sys

# Third-party modules
import aiohttp
import asyncio
import discord
import discord.ext.commands as commands

# Bundled modules
import checks
import errors
from environment import *
import helpers
import cogs.core
import cogs.mod
import cogs.web

assert (sys.version_info >= (3,5)), "This program requires Python 3.5 or higher."

# Constants

APP_NAME = "kitsuchan-ng"
APP_URL = "https://github.com/n303p4/kitsuchan-ng"
APP_VERSION = (0, 0, 4)
APP_VERSION_STRING = "%s.%s.%s" % APP_VERSION

# Initialization

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = discord.ext.commands.Bot(command_prefix="kit!")
bot.description = "A Discord bot that fetches anime images and does other things."
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
    if isinstance(COMMAND_PREFIX, str):
        bot.command_prefix = COMMAND_PREFIX
    else:
        bot.command_prefix = bot.user.name[:3].lower() + "!"
    app_info = await bot.application_info()
    bot.owner = app_info.owner
    game = discord.Game()
    game.name = bot.command_prefix + "help"
    await bot.change_presence(game=game)
    logger.info("Bot is ONLINE! Username: %s, User ID: %s", bot.user.name, bot.user.id)

@bot.event
async def on_command_error(exception, ctx):
    """Handle errors that occur in commands."""
    if isinstance(exception, discord.ext.commands.CheckFailure):
        logger.info("%s (%s) tried to issue a command but was denied." % (ctx.author.name,
                                                                          ctx.author.id))
    # Add more specificity to this at some point.
    else:
        logger.info(str(exception))

if __name__ == "__main__":
    logger.info("Warming up...")
    bot.add_cog(cogs.core.Core(bot, logger))
    bot.add_cog(cogs.mod.Moderation(bot, logger))
    bot.add_cog(cogs.web.Web(bot, logger, API_KEY_IBSEARCH))
    bot.run(API_KEY_DISCORD)
