#!/usr/bin/env python3

"""Helper functions for kitsuchan-ng."""

# Third-party modules
import discord

# Bundled modules
import errors

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
            message = "I don't have permission to do that."
            await ctx.send(message)
            raise errors.BotPermissionsError(message)
            break

async def generate_help_embed_group(group):
    """A helper function to generate help for a group.
    
    Accepts a discord.ext.commands.Group as argument and returns a discord.Embed"""
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
            embed.add_field(name="%s %s" % (group.name, command.name), value=value)
        except AttributeError:
            pass
    return embed
