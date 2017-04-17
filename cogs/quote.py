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

    def scan_embed_didsay(self, dict_embed:dict, quote:str):
        """A recursive helper function that scans embeds for quote. Not case-sensitive."""
        quotes = []
        for value in dict_embed.values():
            if isinstance(value, str) and quote.lower() in value.lower():
                quotes.append(value)
            elif isinstance(value, dict):
                quotes += self.scan_embed_didsay(value, quote)
            elif isinstance(value, list):
                for subvalue in value:
                    if isinstance(subvalue, dict):
                        quotes += self.scan_embed_didsay(subvalue, quote)
        return quotes

    @commands.command()
    async def didsay(self, ctx, user:discord.Member, *, quote=""):
        """Checks if a user said a particular phrase.
        
        * user - A member to mention.
        * *phrase - Command checks against this to see what was said.
        """
        logger.info(f"Checking if someone said \"{quote}\".")
        paginator = commands.Paginator()
        length = 0
        async for message in ctx.channel.history(reverse=True):
            if message.author.id == user.id:
                if quote.lower() in message.content.lower():
                    paginator.add_line(f"{message.created_at.ctime()}: {message.content}")
                for embed in message.embeds:
                    quotes_embed = self.scan_embed_didsay(embed.to_dict(), quote.lower())
                    for quote_embed in quotes_embed:
                        paginator.add_line(f"{message.created_at.ctime()}: {quote_embed}")
            length += 1
        if len(paginator.pages) == 0:
            await ctx.send((f"{user.name} did not say **{quote}** in the last {length} messages. "
                           "Or it was deleted."))
        else:
            await ctx.send(f"Times where {user.name} said **{quote}** in the last {length} messages:")
            for page in paginator.pages:
                await ctx.send(page)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Utilities())
