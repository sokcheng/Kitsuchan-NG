#!/usr/bin/env python3

"""Helper functions for kitsuchan-ng. These DO have discord.py dependencies."""

# Standard modules
import asyncio

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import utils

async def function_by_mentions(ctx, func, pass_member_id:bool=False, *args, **kwargs):
    """A generic helper function that executes a function on all members listed in a context.
    
    ctx - The context for which the function is to be applied.
    func - The function to execute. Function must accept discord.Member or discord.Member.id.
    pass_member_id - Boolean. If true, then member IDs will be passed to func.
                     If false, then member objects will be passed to func.
    *args - A list of additional arguments that func accepts.
    **kwargs - A list of additional keyword arguments that func accepts."""
    if len(ctx.message.mentions) == 0:
        message = "No user(s) were mentioned."
        raise commands.UserInputError(message)
    for member in ctx.message.mentions:
        if pass_member_id:
            await func(member.id, *args, **kwargs)
        else:
            await func(member, *args, **kwargs)

def generate_help_embed(thing):
    """A helper function to generate help for an object.
    
    Accepts anything as an argument and returns a discord.Embed generating help for it.
    
    Currently, this only accepts discord.ext.commands.Group."""
    if isinstance(thing, commands.Group):
        embed = discord.Embed(title=thing.name)
        try:
            embed.description = thing.help
        except AttributeError:
            pass
        if len(thing.aliases) > 0:
            aliases = ", ".join(thing.aliases)
            embed.add_field(name="Aliases", value=aliases, inline=False)
        for command in tuple(thing.commands)[::-1]:
            try:
                if command.hidden:
                    continue
                # Check to see if there's a brief version of the help. If not, make your own.
                if not command.brief:
                    value = str(command.help).split("\n")[0]
                else:
                    value = command.brief
                embed.add_field(name=f"{thing.name} {command.name}", value=value)
            except AttributeError:
                pass
        return embed

async def yes_no(ctx, client:discord.Client,
                 message:str="Are you sure? Type **yes** within 10 seconds to confirm. o.o"):
    """Yes no helper. Ask a confirmation message with a timeout of 10 seconds.
    
    ctx - The context in which the question is being asked.
    client - The client handling the question responses.
    message - Optional messsage that the question should ask.
    """
    await ctx.send(message)
    try:
        message = await client.wait_for("message", timeout=10,
                                        check=lambda message: message.author == ctx.message.author)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting. :<")
        return False
    if message.clean_content.lower() != "yes":
        await ctx.send("Command cancelled. :<")
        return False
    return True

async def input_number(ctx, client:discord.Client,
                       message:str="Please enter a number within 10 seconds."):
    """Input number helper. Ask a confirmation message with a timeout of 10 seconds.
    
    ctx - The context in which the question is being asked.
    client - The client handling the question responses.
    message - Optional messsage that the question should ask.
    """
    await ctx.send(message)
    try:
        message = await client.wait_for("message", timeout=10,
                                        check=lambda message: message.author == ctx.message.author)
    except asyncio.TimeoutError:
        raise commands.UserInputError("Timed out waiting.")
    try:
        return int(message.clean_content.lower())
    except ValueError:
        raise commands.UserInputError("Not a valid number.")

def count_humans(guild:discord.Guild):
    """Tally the humans in a guild."""
    num_humans = len(tuple(filter(lambda member: not member.bot, guild.members)))
    return num_humans

def count_bots(guild:discord.Guild):
    """Tally the bots in a guild."""
    num_bots = len(tuple(filter(lambda member: member.bot, guild.members)))
    return num_bots

def is_moderator(ctx:commands.Context, member:discord.Member):
    """Check member permissions to decide if they're a moderator."""
    if ctx.channel.permissions_for(member).manage_messages \
    and ctx.channel.permissions_for(member).kick_members \
    and ctx.channel.permissions_for(member).ban_members \
    and not member.bot:
        return True
    return False

def has_scanning(ctx:commands.Context):
    """Checks if the current context has image scanning enabled."""
    if (ctx.guild and ctx.guild.explicit_content_filter.name == "disabled")\
    or (hasattr(ctx.channel, "is_nsfw") and ctx.channel.is_nsfw()):
        return False
    return True

def get_emoji(ctx, expression:str):
    """Doesn't really work that well."""
    bot = ctx.bot
    try:
        return bot.get_emoji(int(expression))
    except Exception:
        pass
    expression = expression.strip(":").lower()
    for closeness in range(0, 4):
        for emoji in bot.emojis:
            if utils.levenshtein(expression, emoji.name.lower()) == closeness:
                return emoji
