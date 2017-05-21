#!/usr/bin/env python3

"""Contains a cog for random numbers and stuff."""

# Standard library
import logging
import os
import random
import re

# Third-party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

SIDES_COIN = (":fox: Heads!", ":comet: Tails!")

REGEX_DND = "[0-9]+[dD][0-9]+"
REGEX_DND_SPLIT = "[dD]"
REGEX_OBJECT_DND = re.compile(REGEX_DND)

MAX_ROLL_COUNT = 20
MAX_DICE_PER_ROLL = 30
MAX_DIE_SIZE = 2000

URL_RANDOM_WORD_API = "http://setgetgo.com/randomword/get.php"

# Instantiate a SystemRandom object to produce cryptographically secure random numbers.
systemrandom = random.SystemRandom()

class Random:
    """Commands that generate things at random."""

    @commands.command(aliases=["cflip", "coinflip"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def coin(self, ctx):
        """Flip a coin."""
        
        choice = systemrandom.choice(SIDES_COIN)
        logger.info(f"Flipped a coin; it's {choice}")
        await ctx.send(choice)

    @commands.command(aliases=["randint"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def rng(self, ctx, start:int=1, end:int=100):
        """Randomly generate a number. Default range 1-100.
        
        * start - Specify the starting number of the range.
        * end - Specify the ending number of the range."""
        
        if start > end:
            start, end = end, start
        
        number = systemrandom.randint(start, end)
        message = f"{number} (random number from {start} to {end})"
        logger.info(message)
        await ctx.send(message)

    @commands.command(aliases=["rword", "randword"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def rwg(self, ctx):
        """Randomly generate a word."""
        
        async with ctx.bot.session.get(URL_RANDOM_WORD_API) as response:
            
            if response.status == 200:
                word = await response.text()
                await ctx.send(word)
            
            else:
                message = "Could not reach API. x.x"
                await ctx.send(message)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def roll(self, ctx, *expressions):
        """Roll some dice, using D&D syntax.
        
        Examples:
        * roll 5d6 - Roll five six sided dice.
        * roll 1d20 2d8 - Roll one twenty sided die, and two eight sided dice."""
        
        rolls = []
        
        paginator = commands.Paginator()
        
        counter = 0
        
        for expression in expressions:
            
            if counter >= MAX_ROLL_COUNT:
                break
            
            elif REGEX_OBJECT_DND.fullmatch(expression):
                expression_parts = re.split(REGEX_DND_SPLIT, expression)
                
                roll = [int(value) for value in expression_parts]
                
                if roll[0] > MAX_DICE_PER_ROLL or roll[1] > MAX_DIE_SIZE:
                    continue
                
                elif roll[1] > 1 and roll[0] >= 1:
                    outcomes = []
                    
                    for times in range(0, roll[0]):
                        outcome = systemrandom.randint(1, roll[1])
                        outcomes.append(str(outcome))
                    
                    outcomes_string = ", ".join(outcomes)
                    rolls.append(f"{expression}: {outcomes_string} ({sum(outcomes)})")
                    
                    counter += 1
        
        if len(rolls) > 0:
            for roll in rolls:
                paginator.add_line(roll)
            
            for page in paginator.pages:
                await ctx.send(page)
        
        else:
            raise commands.UserInputError(("No valid rolls supplied. "
                                           f"Please use D&D format, e.g. `5d6`.\n"
                                           "Individual rolls cannot have more than "
                                           f"`{MAX_DICE_PER_ROLL}` dice, and dice cannot have "
                                           f"more than `{MAX_DIE_SIZE}` sides."))

def setup(bot):
    """Setup function for random."""
    bot.add_cog(Random())
