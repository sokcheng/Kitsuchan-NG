#!/usr/bin/env python3

"""Contains a cog for random numbers and stuff."""

# Standard library
import logging
import random
import re

# Third-party modules
import discord
from discord.ext import commands

SIDES_COIN = (":fox: Heads!", ":comet: Tails!")

REGEX_DND = "[0-9]+[dD][0-9]+"
REGEX_DND_SPLIT = "[dD]"
REGEX_OBJECT_DND = re.compile(REGEX_DND)

MAX_ROLL_COUNT = 20
MAX_DICE_PER_ROLL = 30
MAX_DIE_SIZE = 2000

logger = logging.getLogger(__name__)

# Instantiate a SystemRandom object for cryptographically secure random number generation.
systemrandom = random.SystemRandom()

class Utilities:
    """A dice roller module for the Utilities category."""
    def __init__(self):
        pass
    
    @commands.command(aliases=["coinflip"])
    async def cflip(self, ctx):
        """Flip a coin."""
        choice = systemrandom.choice(SIDES_COIN)
        await ctx.send(choice)
    
    @commands.command(aliases=["randint"])
    async def rng(self, ctx, start:int=1, end:int=100):
        """Randomly generate a number. Default range 1-100.
        
        * start - Specify the starting number of the range.
        * end - Specify the ending number of the range."""
        if start > end:
            start, end = end, start
        number = systemrandom.randint(start, end)
        message = f"Random number from {start} to {end}: {number}"
        logger.info(message)
        await ctx.send(message)
    
    @commands.command()
    async def roll(self, ctx, *expressions):
        """Roll some dice, using D&D syntax.
        
        Examples:
        * roll 5d6 - Roll five six sided dice.
        * roll 1d20 2d8 - Roll one twenty sided die, and two eight sided dice."""
        
        # The former list nests sublists of format [expression, num dice, num sides per die]
        # For example, ["5d6", 5, 6]
        
        # The latter list nests sublists of format [expression, outcome 1, outcome 2, ...]
        # For example, ["5d6", 1, 6, 3, 4, 3]
        list_roll_parameters = []
        list_rolls = []
        
        # Message to be sent. Instantiated as None initially.
        message = None
        
        for expression in expressions:
            if isinstance(expression, str) and REGEX_OBJECT_DND.fullmatch(expression):
                expression_parts = re.split(REGEX_DND_SPLIT, expression)
                # Split the expression into two ints, one for the no. of dice and one for sides.
                # After that, insert the original expression into the front.
                roll_parameters = [int(value) for value in expression_parts]
                roll_parameters.insert(0, expression)
                list_roll_parameters.append(roll_parameters)
        
        if len(list_roll_parameters) == 0:
            message = "No valid rolls given; please use D&D format."
            raise commands.UserInputError(message)
        
        elif len(list_roll_parameters) > MAX_ROLL_COUNT:
            message = "Too many rolls requested."
            raise commands.UserInputError(message)
        
        elif len(list_roll_parameters) != len(expressions):
            message = "Some rolls have been ignored, as they were invalid."
        
        for roll_parameters in list_roll_parameters:
            # Skip overly massive rolls.
            if roll_parameters[1] > MAX_DICE_PER_ROLL or roll_parameters[2] > MAX_DIE_SIZE:
                message = "Some rolls have been ignored, as they were too large."
                continue
            
            # Actually roll the dice now.
            roll = [roll_parameters[0]]
            for times in range(roll_parameters[1]):
                roll.append(systemrandom.randint(1, roll_parameters[2]))
            list_rolls.append(roll)
        
        if len(list_rolls) == 0:
            message = "Your rolls have been ignored, as they were too large."
            raise commands.UserInputError(message)
        
        embed = discord.Embed(title="Rolls")
        
        for roll in list_rolls:
            roll_string = ", ".join([str(value) for value in roll[1:]])
            roll_sum_string = str(sum(roll[1:]))
            embed.add_field(name=f"{roll_string} ({roll_sum_string})", value=roll[0])
        
        logger.info("Rolling some dice.")
        await ctx.send(message, embed=embed)

def setup(bot):
    """Setup function for random."""
    bot.add_cog(Utilities())
