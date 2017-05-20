#!/usr/bin/env python3

"""The bot's opinions on stupid crap."""

# Standard modules
import logging
import random

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import utils

logger = logging.getLogger(__name__)

class Opinions:
    """Commands that give the bot's opinion on something."""

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def choose(self, ctx, *, choices=""):
        """Choose between one of various supplied things.
        
        Syntax:
        
        * choose x, y, z - Choose between x, y, and z.
        """
        choices = choices.split(",")
        if len(choices) <= 1:
            raise commands.UserInputError(("Not enough choices! "
                                           "Separate choices with commas, e.g. "
                                           "`choose A cat, A bear, A python`"))
        # Eliminate leading and trailing whitespace.
        for index in range(0, len(choices)):
            choices[index] = choices[index].strip()
        choice = None
        # Loaded choice. The program biases in favor of pythons.
        for distance in range(0, 3):
            for choice_loaded in choices:
                if utils.levenshtein("python", choice_loaded.lower()) == distance:
                    python = (f"{choice_loaded}, obviously",
                              f"{choice_loaded}, duh",
                              choice_loaded)
                    choice = random.choice(python)
                    break
            if choice:
                break
        # Couldn't find a python, so now the program actually choses randomly.
        if not choice:
            choice = random.choice(choices)
        logger.info(f"Chose {choice}")
        await ctx.send(choice)

def setup(bot):
    """Setup function for Reactions."""
    bot.add_cog(Opinions())
