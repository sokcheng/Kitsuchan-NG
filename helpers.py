#!/usr/bin/env python3

"""Helper functions for kitsuchan-ng."""

# Standard modules
import asyncio

# Third-party modules
import discord
from discord.ext import commands

async def function_by_mentions(ctx, func, pass_member_id:bool=False, *params):
    """A generic helper function that executes a function on all members listed in a context.
    
    func - The function you desire to run. Must accept either discord.Member or discord.Member.id.
    pass_member_id - Boolean. If true, then member IDs will be passed to func.
                     If false, then member objects will be passed to func.
    *params - A list of additional parameters to be passed to func."""
    if len(ctx.message.mentions) == 0:
        message = "No user(s) were mentioned."
        raise commands.UserInputError(message)
    for member in ctx.message.mentions:
        if pass_member_id:
            await func(member.id, *params)
        else:
            await func(member, *params)

async def generate_help_embed(group):
    """A helper function to generate help for a group.
    
    Accepts a discord.ext.commands.Group as argument and returns a discord.Embed"""
    if type(group) is commands.Group:
        embed = discord.Embed(title=group.name)
        try:
            embed.description = group.help
        except AttributeError:
            pass
        for command in tuple(group.commands)[::-1]:
            try:
                if command.hidden:
                    continue
                # Check to see if there's a brief version of the help. If not, make your own.
                if not command.brief:
                    value = str(command.help).split("\n")[0]
                else:
                    value = command.brief
                embed.add_field(name=f"{group.name} {command.name}", value=value)
            except AttributeError:
                pass
        return embed

# Yes-no question.
async def yes_no(ctx, client:discord.Client, message:str="Are you sure? Type yes to confirm."):
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
