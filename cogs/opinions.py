#!/usr/bin/env python3

"""The bot's opinions on stupid crap."""

# Standard modules
import logging
import random

# Third-party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Fun:
    """discord.py cog containing functions that give the bot's opinion on something."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx, *choices):
        """Choose between one of various supplied things.
        
        Syntax:
        choose x | y | z - Choose between x, y, and z.
        """
        choices = " ".join(choices).split(" | ")
        if len(choices) <= 1:
            raise commands.UserInputError("Not enough choices specified. Separate choices with |")
        choice = None
        for choice_loaded in choices:
            if "python" in choice_loaded.lower():
                python = (f"{choice_loaded}, obviously",
                          f"{choice_loaded}, duh",
                          choice_loaded)
                choice = random.choice(python)
                break
        if not choice:
            choice = random.choice(choices)
        title = f"{self.bot.user.display_name} chooses:"
        embed = discord.Embed(title=title, description=choice)
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function for Reactions."""
    bot.add_cog(Fun(bot))
