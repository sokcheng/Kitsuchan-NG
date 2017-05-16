#!/usr/bin/env python3

"""Contains a cog for a Magic 8-Ball."""

# Standard modules
import logging
import random

# Third-party modules
from discord.ext import commands

logger = logging.getLogger(__name__)

systemrandom = random.SystemRandom()

ANSWERS = [# Stock replies.
           "It it certain.",
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
           "Very doubtful.",
           
           # Kitsuchan replies
           "Yay!",
           ":fox:",
           ":sunny: :3",
           ":clap:",
           "Kon kon!",
           "+1",
           "Awau! :3",
           ":thumbsup:",
           "Yes. :3",
           ":3",
           
           "Awau? o.o",
           "Ask again later?",
           "/mobileshrug",
           "Don't know? :<",
           "Kon kon kon.",
           
           "Awau. :<",
           "Get bent. :3",
           "No. :<",
           ":thumbsdown:",
           "RIP"]

class Eightball:
    """Magic Eight Ball command."""
    @commands.command(name="8ball", aliases=["eightball"])
    @commands.cooldown(6, 6, commands.BucketType.channel)
    async def _eightball(self, ctx, *, question=""):
        """Ask the Magic 8-Ball a question.
        
        * question - The question to ask. Must end in a ?"""
        if len(question) == 0 or not question.endswith("?"):
            message = "Please specify a question."
            logger.warning(message)
            raise commands.UserInputError(message)
        choice = systemrandom.choice(ANSWERS)
        logger.info(f"Magic 8-Ball answer: {choice}")
        await ctx.send(choice)

def setup(bot):
    """Setup function for 8ball."""
    bot.add_cog(Eightball())
