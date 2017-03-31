#!/usr/bin/env python3

"""Retrieve anime images and do other stuff with a Discord bot.

This is free and unencumbered software released into the public domain, under the Creative Commons
CC0 1.0 Universal Public Domain Dedication.

URL to legal text: https://creativecommons.org/publicdomain/zero/1.0/legalcode

Usage::

Required environment variables:
* OAUTH_TOKEN_DISCORD - OAuth token for Discord.

Optional environment variables:
* API_KEY_IBSEARCH - API key for IbSear.ch.
* COMMAND_PREFIX - Override the bot's command prefix.
* WHITELIST_NSFW - List of channels to allow NSFW content on.
"""

# Standard modules
import logging
import sys

# Third-party modules
import aiohttp
import asyncio
import discord

# Bundled modules
from environment import *
from app_info import *
import cogs.core
import cogs.mod
import cogs.web

assert (sys.version_info >= (3,5)), "This program requires Python 3.5 or higher."
assert (discord.version_info >= (1,0)), "This program requires Discord 1.0 or higher."

# Initialization

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = discord.ext.commands.Bot(command_prefix="kit!", pm_help=True)
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
    bot.add_cog(cogs.web.Web(bot, logger))
    bot.run(OAUTH_TOKEN_DISCORD)
