#!/usr/bin/env python3

"""Contains a cog with commands that quote people."""

# Standard modules
import logging
import random

# Third party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Utilities:
    """discord.py cog containing commands that quote people."""
    
    def __init__(self):
        pass
        
    @commands.command()
    async def quote(self, ctx, user:discord.Member):
        """Quote a user.
        
        * user - The user you wish to quote.
        """
        logger.info("Quoting a user.")
        quotes = []
        async for message in ctx.channel.history():
            if message.author.id == user.id:
                quotes.append(message)
        if len(quotes) == 0:
            await ctx.send("Could not quote that user.")
        else:
            message = random.choice(quotes)
            quote = f"**{user.name} said:**\n{message.content}"
            await ctx.send(quote)
            if len(message.embeds) > 0:
                for embed in message.embeds:
                    await ctx.send(embed=embed)

    @commands.command()
    async def didsay(self, ctx, user:discord.Member, *phrase):
        """Checks if a user said a particular phrase.
        
        * user - A member to mention.
        * *phrase - Command checks against this to see what was said.
        """
        quote = " ".join(phrase)
        logger.info(f"Checking if someone said \"{quote}\".")
        if len(quote) == 0:
            raise commands.UserInputError("A quote was not specified.")
        # Generate a list of quotes to append to the embed.
        quotes = []
        length = 0
        async for message in ctx.channel.history():
            if message.author.id == user.id and quote.lower() in message.content.lower():
                quotes.append((message.created_at, message.content))
            length += 1
        if len(quotes) == 0:
            await ctx.send((f"{user.name} did not say **{quote}** in the last {length} messages. "
                           "Or it was deleted."))
        else:
            title = f"Yes, {user.name} did say __{quote}__."
            embed = discord.Embed(title=title)
            times = 0
            for message in reversed(quotes):
                if times == 25:
                    break
                embed.add_field(name=message[0].ctime(), value=message[1][:1024])
                times += 1
            await ctx.send(embed=embed)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Utilities())
