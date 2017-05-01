#!/usr/bin/env python3

"""This cog checks who plays a certain game."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import errors

logger = logging.getLogger(__name__)

class Playing:
    """Wikipedia command."""

    @commands.command(aliases=["games"])
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def cgames(self, ctx):
        """List all games currently being played in the current guild."""
        players = {}
        for member in ctx.guild.members:
            if member.game and not member.bot:
                players.setdefault(member.game.name, 0)
                players[member.game.name] += 1
        if len(players) == 0:
            await ctx.send(f"Nobody in this guild is playing anything. :<")
            return
        sorted_players = sorted(players.items(), key=lambda item: item[1])
        paginator = commands.Paginator()
        for player in sorted_players:
            if player[1] > 1:
                plural = "s"
            else:
                plural = ""
            paginator.add_line(f"{player[1]} player{plural} of {player[0]}")
        for page in paginator.pages:
            await ctx.send(page)

    @commands.command(aliases=["playing"])
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def whoplays(self, ctx, *, game_name:str):
        """List all members in the current guild playing a game.
        
        * game_name - The game to be checked.
        """
        game_name = game_name.lower()
        players = []
        for member in ctx.guild.members:
            if member.game and member.game.name.lower() == game_name and not member.bot:
                players.append(member)
        if len(players) == 0:
            await ctx.send(f"Nobody in this guild is playing **{game_name}**. :<")
            return
        elif len(players) > 1:
            plural = "s"
        else:
            plural = ""
        paginator = commands.Paginator(prefix="```py")
        paginator.add_line(f"Found {len(players)} member{plural} playing {game_name}:")
        for player in players:
            paginator.add_line(f"{player.name}#{player.discriminator}")
        for page in paginator.pages:
            await ctx.send(page)

def setup(bot):
    """Setup function for Playing."""
    bot.add_cog(Playing())
