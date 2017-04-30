#!/usr/bin/env python3

"""Contains a cog with the bot's invite command."""

# Standard library
import logging

# Third party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Invite:
    """Invite command."""

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def invite(self, ctx):
        """Generate an invite link for this bot."""
        invite_minimal = ("[Minimal invite](https://discordapp.com/oauth2/authorize?"
                          f"client_id={ctx.bot.user.id}&scope=bot)")
        invite_full = ("[Invite with permissions](https://discordapp.com/oauth2/authorize?"
                       f"permissions=93190&client_id={ctx.bot.user.id}&scope=bot)")
        embed = discord.Embed(title="Invite me to your guild with either of the following links!")
        embed.description = "\n".join((invite_minimal, invite_full))
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function for Invite."""
    bot.add_cog(Invite())
