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
import json
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

assert (sys.version_info >= (3,5)), "This program requires Python 3.5 or higher."

APP_NAME = "kitsuchan-ng"
APP_URL = "https://github.com/n303p4/kitsuchan-ng"
APP_VERSION = (0, 0, 3)
APP_VERSION_STRING = "%s.%s.%s" % APP_VERSION

API_KEY_DISCORD = os.environ["API_KEY_DISCORD"]
API_KEY_IBSEARCH = os.environ["API_KEY_IBSEARCH"]
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", None)
WHITELIST_NSFW = os.environ.get("WHITELIST_NSFW", [])

BASE_URL_DUCKDUCKGO = "https://duckduckgo.com/?%s"

BASE_URL_IBSEARCH = "https://ibsear.ch/api/v1/images.json?%s"
BASE_URL_IBSEARCH_IMAGE = "https://%s.ibsear.ch/%s"
BASE_URL_IBSEARCH_XXX = "https://ibsearch.xxx/api/v1/images.json?%s"
BASE_URL_IBSEARCH_XXX_IMAGE = "https://%s.ibsearch.xxx/%s"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = discord.ext.commands.Bot(command_prefix="kit!")
bot.description = "A Discord bot that fetches anime images and does other things."
bot.session = aiohttp.ClientSession(loop=bot.loop)

def check_if_bot_owner(ctx):
    """Check whether the sender of a message is marked as the bot's owner."""
    if ctx.author.id == bot.owner.id:
        return True
    return False

def check_if_channel_admin(ctx):
    """Check whether the sender of a message is marked as a channel admin.""" 
    if ctx.channel.permissions_for(ctx.author).administrator == True \
    or ctx.author.id == ctx.guild.owner.id:
        return True
    return False

@bot.check
def is_human(ctx):
    """Check whether the sender of a message is a human or a bot."""
    return not ctx.author.bot

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
    elif isinstance(exception, errors.ZeroDataLengthError):
        logger.info(str(exception))
    # Add more specificity to this at some point.
    else:
        logger.info(str(exception))

@bot.group(aliases=["i"], invoke_without_command=True)
async def info(ctx):
    """Command group for information commands."""
    embed = discord.Embed(title=info.name)
    embed.description = info.help
    for command in info.commands:
        try:
            command.brief
        except AttributeError:
            pass
        else:
            embed.add_field(name="%s %s" % (info.name, command.name), value=command.brief)
    await ctx.send(embed=embed)

@info.command(brief="Display bot information.", aliases=["a"])
async def about(ctx):
    """Display information about this bot, such as library versions."""
    logger.info("Displaying info about me.")
    embed = discord.Embed(title=APP_NAME)
    embed.url = APP_URL
    embed.description = bot.description
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Version", value=APP_VERSION_STRING)
    embed.add_field(name="Python", value="%s.%s.%s" % sys.version_info[:3])
    embed.add_field(name="discord.py", value=discord.__version__)
    await ctx.send(embed=embed)

@info.command(brief="Display guild information.", aliases=["s"])
async def guild(ctx):
    """Display information about the current guild, such as owner, region, emojis, and roles."""
    logger.info("Displaying info about guild.")
    guild = ctx.guild
    if guild is None:
        raise errors.ContextError("Not in a guild.")
    embed = discord.Embed(title=guild.name)
    embed.description = str(guild.id)
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Owner", value=guild.owner.name)
    embed.add_field(name="Members", value=str(guild.member_count))
    count_channels = str(len(tuple(0 for x in guild.channels if isinstance(x, discord.TextChannel))))
    embed.add_field(name="Text channels", value=count_channels)
    count_channels_voice = str(len(tuple(0 for x in guild.channels if isinstance(x, discord.VoiceChannel))))
    embed.add_field(name="Voice channels", value=count_channels_voice)
    embed.add_field(name="Region", value=str(guild.region))
    embed.add_field(name="Created at", value=guild.created_at.ctime())
    emojis = ", ".join((emoji.name for emoji in guild.emojis))
    if len(emojis) > 0:
        embed.add_field(name="Custom emojis", value=emojis)
    roles = ", ".join((role.name for role in guild.roles))
    embed.add_field(name="Roles", value=roles, inline=False)
    await ctx.send(embed=embed)

@info.command(brief="Display channel info.", aliases=["c"])
async def channel(ctx):
    """Display information about the current channel."""
    logger.info("Displaying info about channel.")
    channel = ctx.channel
    if channel is None:
        raise errors.ContextError()
    embed = discord.Embed(title="#%s" % (channel.name,))
    try:
        channel.topic
    except AttributeError:
        pass
    else:
        embed.description = channel.topic
    embed.add_field(name="Channel ID", value=str(channel.id))
    try:
        channel.guild
    except AttributeError:
        pass
    else:
        embed.add_field(name="Guild", value=channel.guild.name)
    embed.add_field(name="Created at", value=channel.created_at.ctime())
    if str(channel.id) in WHITELIST_NSFW:
        embed.set_footer(text="NSFW content is enabled for this channel.")
    await ctx.send(embed=embed)

@info.command(brief="Display user info.", aliases=["u"])
async def user(ctx):
    """Display information about you, such as status and roles.
    
    Mention a user while invoking this command to display information about that user."""
    logger.info("Displaying info about user.")
    try:
        user = ctx.message.mentions[0]
    except IndexError:
        user = ctx.author
    embed = discord.Embed(title=user.display_name)
    if user.display_name != user.name:
        embed.description = user.name
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="User ID", value=str(user.id))
    if user.bot:
        embed.add_field(name="Bot?", value="Yes")
    status = str(user.status).capitalize()
    if status == "Dnd":
        status = "Do Not Disturb"
    embed.add_field(name="Status", value=status)
    if user.game:
        embed.add_field(name="Playing", value=user.game.name)
    embed.add_field(name="Joined guild at", value=user.joined_at.ctime())
    embed.add_field(name="Joined Discord at", value=user.created_at.ctime())
    roles = ", ".join((str(role) for role in user.roles))
    embed.add_field(name="Roles", value=roles, inline=False)
    await ctx.send(embed=embed)

@bot.command(brief="Repeat the user's text back at them.", aliases=["say"])
async def echo(ctx, *text):
    """Repeat the user's text back at them.
    
    *text - A list of strings, which is concatenated into one string before being echoed.
    """
    await ctx.send(" ".join(text))

@bot.command(brief="Retrieve an answer from DuckDuckGo.", aliases=["ddg"])
async def duckduckgo(ctx, *query):
    """Retrieve an answer from DuckDuckGo, using the Instant Answers JSON API.
    
    *query - A list of strings to be used in the search criteria.
    
    This command is extremely versatile! Here are a few examples of things you can do with it:
    
    >> ddg roll 5d6 - Roll five 6-sided dice.
    >> ddg 40 f in c - Convert 40 degrees Fahrenheit to Celsius.
    >> ddg (5+6)^2/4 - Produces 30.25.
    >> ddg random number 1 100 - Generate a random number from 1 to 100.
    >> ddg random name - Generate a random name.
    >> ddg random fortune - Generate a random fortune.
    """
    logger.info("Retrieving DuckDuckGo answer with tags %s." % (query,))
    query_search = " ".join(query)
    params = urllib.parse.urlencode({"q": query_search, "t": "ffsb",
                                     "format": "json", "ia": "answer"})
    url = BASE_URL_DUCKDUCKGO % params
    async with bot.session.get(url) as response:
        if response.status == 200:
            # This should be response.json() directly, but DuckDuckGo returns an incorrect MIME.
            data = await response.text()
            data = json.loads(data)
            if len(data) == 0:
                # I wanted to put statements like this in on_command_error.
                # However, it seems not to work when the ctx.send is in an elif block. :/
                await ctx.send("Could not find any results.")
                raise errors.ZeroDataLengthError()
            answer = html.unescape(data.get("Answer"))
            embed = discord.Embed(title=answer)
            params_short = urllib.parse.urlencode({"q": query_search})
            embed.description = BASE_URL_DUCKDUCKGO % params_short
            await ctx.send(embed=embed)
            logger.info("Answer retrieved!")
        else:
            message = "Failed to fetch answer. :("
            await ctx.send(message)
            logger.info(message)

@bot.command(brief="Fetch an image from IbSear.ch.", aliases=["ib"])
async def ibsearch(ctx, *tags):
    """Retrieve a randomized image from IbSear.ch.
    
    *tags - A list of tag strings to be used in the search criteria.
    
    This command accepts common imageboard tags and keywords. Here are a few examples:
    
    >> ib red_hair armor - Search for images tagged with either red_hair or armor.
    >> ib +animal_ears +armor - Search for images tagged with both red_hair and armor.
    >> ib 1280x1024 - Search for images that are 1920x1080.
    >> ib 5:4 - Search for images in 5:4 aspect ratio.
    >> ib random: - You don't care about what you get."""
    logger.info("Fetching image with tags %s." % (tags,))
    if str(ctx.channel.id) in WHITELIST_NSFW:
        logger.info("NSFW allowed for channel %s." % (ctx.channel.id,))
        base_url = BASE_URL_IBSEARCH_XXX
        base_url_image = BASE_URL_IBSEARCH_XXX_IMAGE
    else:
        logger.info("NSFW disallowed for channel %s." % (ctx.channel.id,))
        base_url = BASE_URL_IBSEARCH
        base_url_image = BASE_URL_IBSEARCH_IMAGE
    query_tags = " ".join(tags)
    params = urllib.parse.urlencode({"key": API_KEY_IBSEARCH, "q": query_tags})
    url = base_url % params
    async with bot.session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if len(data) == 0:
                await ctx.send("Could not find any results.")
                raise errors.ZeroDataLengthError()
            index = random.randint(1, len(data)) - 1
            result = data[index]
            embed = discord.Embed()
            url_image = base_url_image % (data[index]["server"], data[index]["path"])
            embed.description = url_image
            embed.set_image(url=url_image)
            await ctx.send(embed=embed)
            logger.info("Image retrieved!")
        else:
            message = "Failed to fetch image. :("
            await ctx.send(message)
            logger.info(message)

@bot.command(brief="Halt the bot.", aliases=["h"])
@commands.check(check_if_bot_owner)
async def halt(ctx):
    """Halt the bot. Must be bot owner to execute."""
    logger.warning("Halting bot!")
    await ctx.send("Halting.")
    await bot.logout()
    bot.session.close()

@bot.command(brief="Restart the bot.", aliases=["r"])
@commands.check(check_if_bot_owner)
async def restart(ctx):
    """Restart the bot. Must be bot owner to execute."""
    logger.warning("Restarting bot!")
    await ctx.send("Restarting.")
    await bot.logout()
    bot.session.close()
    os.execl(os.path.realpath(__file__), *sys.argv)

if __name__ == "__main__":
    logger.info("Warming up...")
    bot.run(API_KEY_DISCORD)
