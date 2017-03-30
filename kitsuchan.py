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
import html
import logging
import random
import sys
import urllib.parse

# Third-party modules
import aiohttp
import asyncio
import discord
import discord.ext.commands as commands

# Bundled modules
import errors

APP_NAME = "kitsuchan-ng"
APP_URL = "https://github.com/n303p4/kitsuchan-ng"
APP_VERSION = (0, 0, 2)
APP_VERSION_STRING = "%s.%s.%s" % APP_VERSION

API_KEY_DISCORD = os.environ["API_KEY_DISCORD"]
API_KEY_IBSEARCH = os.environ["API_KEY_IBSEARCH"]
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", None)
WHITELIST_NSFW = os.environ.get("WHITELIST_NSFW", [])

BASE_URL_DUCKDUCKGO = "https://duckduckgo.com/?%s"

BASE_URL_IBSEARCH = "https://ibsear.ch/api/v1/images.json?%s"
BASE_URL_IBSEARCH_IMAGE = "https://im1.ibsear.ch/%s"
BASE_URL_IBSEARCH_XXX = "https://ibsearch.xxx/api/v1/images.json?%s"
BASE_URL_IBSEARCH_XXX_IMAGE = "https://im1.ibsearch.xxx/%s"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = discord.ext.commands.Bot(command_prefix="kit!")
bot.description = "A Discord bot that fetches anime images and does other things."
bot.session = aiohttp.ClientSession(loop=bot.loop)

def check_if_bot_owner(ctx):
    """Check whether the sender of a message is marked as the bot's owner."""
    if ctx.message.author.id == bot.owner.id:
        return True
    return False

def check_if_channel_admin(ctx):
    """Check whether the sender of a message is marked as a channel admin.""" 
    if ctx.message.channel.permissions_for(ctx.message.author).administrator == True \
    or ctx.message.author.id == ctx.server.owner.id:
        return True
    return False

@bot.check
def is_human(ctx):
    """Check whether the sender of a message is a human or a bot."""
    return not ctx.message.author.bot

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
        logger.info("%s (%s) tried to issue a command but was denied." % (ctx.message.author.name,
                                                                          ctx.message.author.id))
    # Add more specificity to this at some point.
    else:
        logger.info(str(exception))

@bot.group(brief="Command group for info. Run help info for details.", aliases=["i"],
           help=("Command group for a series of more specific commands. Does not do anything if "
                 "you run it by itself."))
async def info():
    """Do nothing, but act as a placeholder for several subcommands."""
    pass

@info.command(brief="Display bot info.", aliases=["m"],
              help=("Display information about the bot. Mainly useful for version info."))
async def me():
    """Display bot info."""
    logger.info("Displaying info about me.")
    embed = discord.Embed(title=APP_NAME)
    embed.url = APP_URL
    embed.description = bot.description
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Version", value=APP_VERSION_STRING)
    embed.add_field(name="discord.py", value=discord.__version__)
    await bot.say(embed=embed)

@info.command(brief="Display server info.", aliases=["s"], pass_context=True,
              help=("Display information about the current server, such as owner info, region, "
                    "custom emojis, and roles."))
async def server(ctx):
    """Display server info about the current context."""
    logger.info("Displaying info about server.")
    server = ctx.message.server
    if server is None:
        raise errors.ContextError("Not in a server.")
    embed = discord.Embed(title=server.name)
    embed.description = server.id
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name="Owner", value=server.owner.name)
    embed.add_field(name="Members", value=str(server.member_count))
    count_channels = str(len(tuple(0 for x in server.channels if str(x.type) == "text")))
    embed.add_field(name="Text channels", value=count_channels)
    count_channels_voice = str(len(tuple(0 for x in server.channels if str(x.type) == "voice")))
    embed.add_field(name="Voice channels", value=count_channels_voice)
    embed.add_field(name="Region", value=str(server.region))
    embed.add_field(name="Created at", value=server.created_at.ctime())
    emojis = ", ".join((emoji.name for emoji in server.emojis))
    if len(emojis) > 0:
        embed.add_field(name="Custom emojis", value=emojis)
    roles = ", ".join((role.name for role in server.roles))
    embed.add_field(name="Roles", value=roles, inline=False)
    await bot.say(embed=embed)

@info.command(brief="Display channel info.", aliases=["c"], pass_context=True,
              help=("Display information about the current channel."))
async def channel(ctx):
    """Display channel info about the current context."""
    logger.info("Displaying info about channel.")
    channel = ctx.message.channel
    if channel is None:
        raise errors.ContextError()
    embed = discord.Embed(title="#%s" % (channel.name,))
    try:
        channel.topic
    except AttributeError:
        pass
    else:
        embed.description = channel.topic
    embed.add_field(name="Channel ID", value=channel.id)
    try:
        channel.server
    except AttributeError:
        pass
    else:
        embed.add_field(name="Server", value=channel.server.name)
    embed.add_field(name="Created at", value=channel.created_at.ctime())
    if channel.id in WHITELIST_NSFW:
        embed.set_footer(text="NSFW content is enabled for this channel.")
    await bot.say(embed=embed)

@info.command(brief="Display user info.", aliases=["u"], pass_context=True,
              help=("Display information about the mentioned user, such as status and roles."))
async def user(ctx):
    """Display info about the first user mentioned in this command."""
    logger.info("Displaying info about user.")
    try:
        user = ctx.message.mentions[0]
    except IndexError:
        raise errors.InputError("No users mentioned.")
    embed = discord.Embed(title=user.display_name)
    if user.display_name != user.name:
        embed.description = user.name
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="User ID", value=user.id)
    if user.bot:
        embed.add_field(name="Bot?", value="Yes")
    status = str(user.status).capitalize()
    if status == "Dnd":
        status = "Do Not Disturb"
    embed.add_field(name="Status", value=status)
    if user.game:
        embed.add_field(name="Playing", value=user.game.name)
    embed.add_field(name="Joined server at", value=user.joined_at.ctime())
    embed.add_field(name="Joined Discord at", value=user.created_at.ctime())
    roles = ", ".join((str(role) for role in user.roles))
    embed.add_field(name="Roles", value=roles, inline=False)
    await bot.say(embed=embed)

@bot.command(help="Repeat the user's text back at them.", aliases=["say"])
async def echo(*text):
    """Repeat the user's text back at them.
    
    *text - A list of strings, which is concatenated into one string before being echoed.
    """
    await bot.say(" ".join(text))

@bot.command(brief="Retrieve an answer from DuckDuckGo.", aliases=["ddg"],
             help=("Query the DuckDuckGo Instant Answers API.\n\n"
                   "This command is extremely versatile! Here are a few examples of things you "
                   "can do with it:\n\n"
                   "ddg roll 5d6 - Roll five 6-sided dice.\n"
                   "ddg 40 f in c - Convert 40 degrees Fahrenheit to Celsius.\n"
                   "ddg (5+6)^2/4 - Produces 30.25.\n"
                   "ddg random number 1 100 - Generate a random number from 1 to 100.\n"
                   "ddg random name - Generate a random name.\n"
                   "ddg random fortune - Generate a random fortune."))
async def duckduckgo(*query):
    """Retrieve an answer from DuckDuckGo, using the Instant Answers JSON API.
    
    *query - A list of strings to be used in the search criteria.
    """
    logger.info("Retrieving DuckDuckGo answer with tags %s." % (query,))
    query_search = " ".join(query)
    params = urllib.parse.urlencode({"q": query_search, "t": "ffsb",
                                     "format": "json", "ia": "answer"})
    url = BASE_URL_DUCKDUCKGO % params
    async with bot.session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if len(data) == 0:
                raise errors.ZeroDataLengthError()
            answer = html.unescape(data.get("Answer"))
            embed = discord.Embed(title=answer)
            params_short = urllib.parse.urlencode({"q": query_search})
            embed.description = BASE_URL_DUCKDUCKGO % params_short
            await bot.say(embed=embed)
            logger.info("Answer retrieved!")
        else:
            message = "Failed to fetch answer. :("
            await bot.say(message)
            logger.info(message)

@bot.command(brief="Fetch an image from IbSear.ch.", aliases=["ib"], pass_context=True,
             help=("Search IbSear.ch for an anime picture. You may pass standard imageboard "
                   "tags as arguments to refine the result a bit."))
async def ibsearch(ctx, *tags):
    """Retrieve a randomized image from IbSear.ch.
    
    *tags - A list of strings to be used in the search criteria.
    """
    logger.info("Fetching image with tags %s." % (tags,))
    if ctx.message.channel.id in WHITELIST_NSFW:
        logger.info("NSFW allowed for channel %s." % (ctx.message.channel.id,))
        base_url = BASE_URL_IBSEARCH_XXX
        base_url_image = BASE_URL_IBSEARCH_XXX_IMAGE
    else:
        logger.info("NSFW disallowed for channel %s." % (ctx.message.channel.id,))
        base_url = BASE_URL_IBSEARCH
        base_url_image = BASE_URL_IBSEARCH_IMAGE
    query_tags = " ".join(tags)
    params = urllib.parse.urlencode({"key": API_KEY_IBSEARCH, "q": query_tags})
    url = base_url % params
    async with bot.session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if len(data) == 0:
                raise errors.ZeroDataLengthError()
            index = random.randint(1, len(data)) - 1
            result = data[index]
            embed = discord.Embed()
            url_image = base_url_image % (data[index]["path"],)
            embed.description = url_image
            embed.set_image(url=url_image)
            await bot.say(embed=embed)
            logger.info("Image retrieved!")
        else:
            message = "Failed to fetch image. :("
            await bot.say(message)
            logger.info(message)

@bot.command(brief="Halt the bot.", aliases=["h"],
             help="End execution of the bot. Can only be done by the bot owner.")
@commands.check(check_if_bot_owner)
async def halt():
    """Halt the bot. Must be bot owner to execute."""
    logger.warning("Halting bot!")
    await bot.say("Halting.")
    await bot.logout()
    bot.session.close()

@bot.command(brief="Restart the bot.", aliases=["r"],
             help="Restart execution of the bot. Can only be done by the bot owner.")
@commands.check(check_if_bot_owner)
async def restart():
    """Restart the bot. Must be bot owner to execute."""
    logger.warning("Restarting bot!")
    await bot.say("Restarting.")
    await bot.logout()
    bot.session.close()
    os.execl(os.path.realpath(__file__), *sys.argv)

if __name__ == "__main__":
    logger.info("Warming up...")
    bot.run(API_KEY_DISCORD)
