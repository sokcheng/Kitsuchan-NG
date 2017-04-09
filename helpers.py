#!/usr/bin/env python3

"""Helper functions for kitsuchan-ng."""

# Standard modules
import asyncio

# Third-party modules
import discord
from discord.ext import commands

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

async def generate_help_embed(thing):
    """A helper function to generate help for an object.
    
    Accepts anything as an argument and returns a discord.Embed generating help for it.
    
    Currently, this only accepts discord.ext.commands.Group."""
    if type(thing) is commands.Group:
        embed = discord.Embed(title=thing.name)
        try:
            embed.description = thing.help
        except AttributeError:
            pass
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

async def yes_no(ctx, client:discord.Client, message:str="Are you sure? Type yes to confirm."):
    """Yes no helper. Ask a confirmation message with a timeout of 5 seconds.
    
    ctx - The context in which the question is being asked.
    client - The client handling the question responses.
    message - Optional messsage that the question should ask.
    """
    embed = discord.Embed(title=message, color=discord.Color.red())
    await ctx.send(embed=embed)
    try:
        message = await client.wait_for("message", timeout=5,
                                        check=lambda message: message.author == ctx.message.author)
    except asyncio.TimeoutError:
        embed = discord.Embed(title="Timed out waiting.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return False
    if message.clean_content.lower() != "yes":
        embed = discord.Embed(title="Command cancelled.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return False
    return True
