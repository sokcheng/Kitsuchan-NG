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
        paginator = commands.Paginator(prefix="```markdown", max_size=375)
        
        for player in sorted_players:
            line = f"{player[1]}. playing {player[0]}"
            line = line.replace("```", "'''")
            paginator.add_line(line)
        
        if len(paginator.pages) == 1:
            await ctx.send(paginator.pages[0])
        
        elif len(paginator.pages) > 1 and not page_number:
            page_number = await helpers.input_number(ctx, ctx.bot,
                                                     ("Please enter a page number from "
                                                      f"1-{len(paginator.pages)}."))
            try:
                await ctx.send(paginator.pages[page_number-1])
            except IndexError:
                raise commands.UserInputError("That page is not valid.")

    @commands.command(aliases=["playing"])
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def whoplays(self, ctx, *, game_name:str):
        """List all members in the current guild playing a game.
        
        * game_name - The game to be checked.
        """
        
        # This implementation is bad.
        players = []
        
        for member in ctx.guild.members:
            if member.game and isinstance(member.game.name, str) \
            and member.game.name.lower() == game_name.lower() and not member.bot:
                players.append(member)
        
        if len(players) == 0:
            await ctx.send(f"Nobody in this guild is playing **{game_name}**. :<")
        
        else:
            paginator = commands.Paginator(prefix="```markdown")
            paginator.add_line(f"# Found {len(players)} player(s) of {game_name} #")
            
            for index in range(0, min(len(players), 10)):
                player = players[index]
                line = f"{index+1}. {player.name}#{player.discriminator}"
                line.replace("```", "'''")
                paginator.add_line(line)
            if len(len(players)) > 10:
                paginator.add_line(f"...and {len(players)-10} others.")
            
            await ctx.send(paginator.pages[0])

def setup(bot):
    """Setup function for Playing."""
    bot.add_cog(Playing())
