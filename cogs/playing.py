#!/usr/bin/env python3

"""This cog checks who plays a certain game."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import errors
import helpers

logger = logging.getLogger(__name__)

class Playing:
    """Wikipedia command."""

    @commands.command(aliases=["games"])
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def cgames(self, ctx, page_number:int=None):
        """List all games currently being played in the current guild.
        
        * page_number - Optional parameter if there are too many pages."""
        players = {}
        for member in ctx.guild.members:
            if member.game and not member.bot:
                players.setdefault(member.game.name, 0)
                players[member.game.name] += 1
        if len(players) == 0:
            await ctx.send(f"Nobody in this guild is playing anything. :<")
            return
        sorted_players = sorted(players.items(), key=lambda item: item[1], reverse=True)
        paginator = commands.Paginator(max_size=375)
        for player in sorted_players:
            if player[1] > 1:
                plural = "s"
            else:
                plural = ""
            line = f"{player[1]} member{plural} playing {player[0]}"
            line = line.replace("```", "'''")
            paginator.add_line(line)
        if len(paginator.pages) == 1:
            await ctx.send(paginator.pages[0])
            return
        if len(paginator.pages) > 1 and not page_number:
            page_number = await helpers.input_number(("Enter a page number from "
                                                      f"(1-{len(paginator.pages)})."))
        try:
            await ctx.send(paginator.pages[page_number-1])
        except IndexError:
            raise commands.UserInputError("That page is not valid. :<")

    @commands.command(aliases=["playing"])
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def whoplays(self, ctx, *, game_name:str):
        """List all members in the current guild playing a game.
        
        * game_name - The game to be checked.
        """
        # This implementation is bad.
        game_name = game_name.lower()
        players = []
        for member in ctx.guild.members:
            if member.game and isinstance(member.game.name, str) \
            and member.game.name.lower() == game_name and not member.bot:
                players.append(member)
        if len(players) == 0:
            await ctx.send(f"Nobody in this guild is playing **{game_name}**. :<")
            return
        elif len(players) > 1:
            plural = "s"
        else:
            plural = ""
        paginator = commands.Paginator(prefix="```py", max_size=375)
        paginator.add_line(f"Found {len(players)} member{plural} playing {game_name}:")
        for player in players:
            line = f"{player.name}#{player.discriminator}"
            line.replace("```", "'''")
            paginator.add_line(line)
        await ctx.send(paginator.pages[0])
        if len(paginator.pages) > 1:
            await ctx.send("...and some others.")

def setup(bot):
    """Setup function for Playing."""
    bot.add_cog(Playing())
