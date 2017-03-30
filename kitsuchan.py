#!/usr/bin/env python3

"""Retrieve anime images with a Discord bot.

Usage::

    >>> Set environment variables API_KEY_DISCORD_KITSUCHAN and API_KEY_IBSEARCH_KITSUCHAN
    >>> Set environment variable WHITELIST_ADMINS_KITSUCHAN as a list of Discord users with admin
    >>> Optionally set WHITELIST_NSFW_KITSUCHAN for channels you wish to whitelist
    >>> kitsuchan.py
"""

# Standard modules
import os
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
APP_VERSION = (0, 0, 1, "alpha", 1)
APP_VERSION_STRING = "%s.%s.%s-%s%s" % APP_VERSION

API_KEY_DISCORD = os.environ["API_KEY_DISCORD_KITSUCHAN"]
API_KEY_IBSEARCH = os.environ["API_KEY_IBSEARCH_KITSUCHAN"]

WHITELIST_ADMINS = os.environ["WHITELIST_ADMINS_KITSUCHAN"]
WHITELIST_NSFW = os.environ.get("WHITELIST_NSFW_KITSUCHAN", [])

BASE_URL_DUCKDUCKGO = "https://duckduckgo.com/?%s"

BASE_URL_IBSEARCH = "https://ibsear.ch/api/v1/images.json?%s"
BASE_URL_IBSEARCH_IMAGE = "https://im1.ibsear.ch/%s"
BASE_URL_IBSEARCH_XXX = "https://ibsearch.xxx/api/v1/images.json?%s"
BASE_URL_IBSEARCH_XXX_IMAGE = "https://im1.ibsearch.xxx/%s"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = discord.ext.commands.Bot(command_prefix="ki!")
bot.description = "A Discord bot that fetches anime images and does other things."
bot.session = aiohttp.ClientSession(loop=bot.loop)

def check_if_admin(ctx):
    if ctx.message.author.id in WHITELIST_ADMINS:
        return True
    return False

@bot.check
def is_human(ctx):
    return not ctx.message.author.bot

@bot.event
async def on_ready():
    bot.command_prefix = bot.user.name[:3].lower() + "!"
    game = discord.Game()
    game.name = bot.command_prefix + "help"
    await bot.change_presence(game=game)
    logger.info("Bot is ONLINE! Username: %s, User ID: %s", bot.user.name, bot.user.id)

@bot.event
async def on_command_error(exception, ctx):
    if isinstance(exception, discord.ext.commands.CheckFailure):
        logger.info("%s (%s) tried to issue a command but was denied." % (ctx.message.author.name,
                                                                          ctx.message.author.id))
    elif isinstance(exception, errors.InputError):
        logger.info(str(exception))
    elif isinstance(exception, errors.ContextError):
        logger.info(str(exception))
    else:
        logger.info(str(exception))

@bot.group(help="Command group for info. ki!help info for details.", aliases=["i"])
async def info():
    pass

@info.command(help="Fetch bot info.", aliases=["m"])
async def me():
    logger.info("Displaying info about me.")
    embed = discord.Embed(title=APP_NAME)
    embed.url = APP_URL
    embed.description = bot.description
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Version", value=APP_VERSION_STRING)
    embed.add_field(name="discord.py", value=discord.__version__)
    await bot.say(embed=embed)

@info.command(help="Fetch server info.", aliases=["s"], pass_context=True)
async def server(ctx):
    logger.info("Displaying info about server.")
    server = ctx.message.server
    if server is None:
        raise errors.ContextError("Not in a server.")
    embed = discord.Embed(title=server.name)
    embed.description = server.id
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name="Owner", value=server.owner.name)
    embed.add_field(name="Members", value=str(server.member_count))
    embed.add_field(name="Region", value=str(server.region))
    embed.add_field(name="Created at", value=server.created_at.ctime())
    emojis = ", ".join((emoji.name for emoji in server.emojis))
    if len(emojis) > 0:
        embed.add_field(name="Custom emojis", value=emojis)
    roles = ", ".join((role.name for role in server.roles))
    embed.add_field(name="Roles", value=roles, inline=False)
    await bot.say(embed=embed)

@info.command(help="Fetch channel info.", aliases=["c"], pass_context=True)
async def channel(ctx):
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

@info.command(help="Fetch channel info.", aliases=["u"], pass_context=True)
async def user(ctx):
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

@bot.command(help="Retrieve an answer from DuckDuckGo.", aliases=["ddg"])
async def duckduckgo(*query):
    logger.info("Retrieving DuckDuckGo answer with tags %s." % (query,))
    query_search = "+".join(urllib.parse.quote(term) for term in query)
    params = urllib.parse.urlencode({"q": query_search, "t": "ffsb",
                                     "format": "json", "ia": "answer"}, safe="+")
    url = BASE_URL_DUCKDUCKGO % params
    async with bot.session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            answer = data.get("Answer")
            embed = discord.Embed(title=answer)
            params_short = urllib.parse.urlencode({"q": query_search}, safe="+")
            embed.description = BASE_URL_DUCKDUCKGO % params_short
            await bot.say(embed=embed)
        else:
            await bot.say("Failed to fetch answer. :(")

@bot.command(help="Fetch an image from IbSear.ch.", aliases=["ib"], pass_context=True)
async def ibsearch(ctx, *tags):
    logger.info("Fetching image with tags %s." % (tags,))
    if ctx.message.channel.id in WHITELIST_NSFW:
        logger.info("NSFW allowed for channel %s." % (ctx.message.channel.id,))
        base_url = BASE_URL_IBSEARCH_XXX
        base_url_image = BASE_URL_IBSEARCH_XXX_IMAGE
    else:
        logger.info("NSFW disallowed for channel %s." % (ctx.message.channel.id,))
        base_url = BASE_URL_IBSEARCH
        base_url_image = BASE_URL_IBSEARCH_IMAGE
    query_tags = "+".join(tags)
    params = urllib.parse.urlencode({"key": API_KEY_IBSEARCH, "q": query_tags}, safe="+")
    url = base_url % params
    print(url)
    async with bot.session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            index = random.randint(1, len(data)) - 1
            result = data[index]
            embed = discord.Embed()
            embed.set_image(url=base_url_image % (data[index]["path"],))
            await bot.say(embed=embed)
        else:
            await bot.say("Failed to fetch images. :(")

@bot.command(help="Halts the bot.", aliases=["h"])
@commands.check(check_if_admin)
async def halt():
    logger.warning("Halting bot!")
    await bot.say("Halting.")
    await bot.logout()
    bot.session.close()

@bot.command(help="Restarts the bot.", aliases=["r"])
@commands.check(check_if_admin)
async def restart():
    logger.warning("Restarting bot!")
    await bot.say("Restarting.")
    await bot.logout()
    bot.session.close()
    os.execl(os.path.realpath(__file__), *sys.argv)

if __name__ == "__main__":
    logger.info("Warming up...")
    bot.run(API_KEY_DISCORD)
