#!/usr/bin/env python3

"""Contains a cog for a Magic 8-Ball."""

# Standard modules
import logging
import random

# Third-party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

ANSWERS = ["It it certain.",
           "It is decidedly so.",
           "Without a doubt.",
           "Yes definitely.",
           "You may rely on it.",
           "As I see it, yes.",
           "Most likely.",
           "Outlook good.",
           "Yes.",
           "Signs point to yes.",
           
           "Reply hazy try again.",
           "Ask again later.",
           "Better not to tell you now.",
           "Cannot predict now.",
           "Concentrate and ask again.",
           
           "Don't count on it.",
           "My reply is no.",
           "My sources say no.",
           "Outlook not so good.",
           "Very doubtful."]

class Fun:
    """discord.py cog containing Rem resource API commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def _eightball(self, ctx, *question):
        """Ask the Magic 8-Ball a question."""
        question = " ".join(question)
        if len(question) == 0 or "?" not in question:
            message = "Please specify a question."
            logger.warning(message)
            raise commands.UserInputError(message)
        choice = random.choice(ANSWERS)
        logger.info(f"Magic 8-Ball queried; answer: {choice}")
        await ctx.send(choice)

def setup(bot):
    """Setup function for 8ball."""
    bot.add_cog(Fun(bot))
