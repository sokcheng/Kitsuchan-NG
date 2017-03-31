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

# Helper functions

async def generate_help_group(group):
    """A helper function to generate help for a group.
    
    Accepts a discord.ext.commands.Group as argument and returns a discord.Embed"""
    embed = discord.Embed(title=group.name)
    try:
        embed.description = group.help
    except AttributeError:
        pass
    for command in tuple(group.commands)[::-1]:
        try:
            embed.add_field(name="%s %s" % (group.name, command.name), value=command.brief)
        except AttributeError:
            pass
    return embed

async def function_by_mentions(ctx, func, pass_member_id:bool, *params):
    """A generic helper function that executes a function on all members listed in a context.
    
    func - The function you desire to run. Must accept either discord.Member or discord.Member.id.
    pass_member_id - Boolean. If true, then member IDs will be passed to func.
                     If false, then member objects will be passed to func.
    *params - A list of additional parameters to be passed to func."""
    if len(ctx.message.mentions) == 0:
        message = "Please mention some member(s)."
        await ctx.send(message)
        raise errors.InputError(ctx.message.mentions, message)
    for member in ctx.message.mentions:
        try:
            if pass_member_id:
                await func(member.id, *params)
            else:
                await func(member, *params)
        except discord.Forbidden as error:
            await ctx.send("I don't have permission to do that.")
            logger.info(error)
            break

# Checking functions

def check_if_bot_owner(ctx):
    """Check whether the sender of a message is marked as the bot's owner."""
    if ctx.author.id == bot.owner.id:
        return True
    return False

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

# Commands

@bot.group(aliases=["i"], invoke_without_command=True)
async def info(ctx):
    """Command group for information commands."""
    embed = await generate_help_group(info)
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
        embed.description = channel.topic
    except AttributeError:
        pass
    embed.add_field(name="Channel ID", value=str(channel.id))
    try:
        embed.add_field(name="Guild", value=channel.guild.name)
    except AttributeError:
        pass
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

@bot.group(brief="Moderation commands", aliases=["m", "moderate"], invoke_without_command=True)
async def mod(ctx):
    """Command group for moderation commands."""
    embed = await generate_help_group(mod)
    await ctx.send(embed=embed)

@mod.command(brief="Kick all users mentioned by this command.")
@commands.check(checks.is_channel_admin)
async def kick(ctx):
    """Kick all users mentioned by this command."""
    await function_by_mentions(ctx, bot.http.kick, True, ctx.guild.id)

@mod.command(brief="Ban all users mentioned by this command.")
@commands.check(checks.is_channel_admin)
async def ban(ctx):
    """Ban all users mentioned by this command."""
    await function_by_mentions(ctx, bot.http.ban, True, ctx.guild.id)

@mod.command(brief="Whitelists channel for NSFW content.", aliases=["nsfw"])
@commands.check(checks.is_channel_admin)
async def permitnsfw(ctx):
    """Whitelists channel for NSFW content.
    
    Is NOT persistent. If the bot restarts, it won't remember this info."""
    if str(ctx.channel.id) not in WHITELIST_NSFW:
        logger.info("NSFW content for %s is now enabled." % (ctx.channel.id,))
        WHITELIST_NSFW.append(str(ctx.channel.id))
        await ctx.send("NSFW content for this channel is now enabled.")
    else:
        await ctx.send("NSFW content is already enabled for this channel.")

@mod.command(brief="Blacklists channel for NSFW content.", aliases=["sfw"])
@commands.check(checks.is_channel_admin)
async def revokensfw(ctx):
    """Whitelists channel for NSFW content.
    
    Is NOT persistent. If the bot restarts, it won't remember this info."""
    if str(ctx.channel.id) in WHITELIST_NSFW:
        logger.info("NSFW content for %s is now disabled." % (ctx.channel.id,))
        WHITELIST_NSFW.remove(str(ctx.channel.id))
        await ctx.send("NSFW content for this channel is now disabled.")
    else:
        await ctx.send("NSFW content is already disabled for this channel.")

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
    bot.add_cog(cogs.web.APIs(bot, logger, API_KEY_IBSEARCH))
    bot.run(API_KEY_DISCORD)
