#!/usr/bin/env python3

"""Contains a cog with the bot's utility commands."""

# Standard modules
import logging

# Third party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Utilities:
    """discord.py cog containing utility functions of the bot.
    
    bot - The parent discord.Client object for the cog.
    logger - A logger to assign the cog.
    """
    
    def __init__(self):
        pass
        
    @commands.command()
    async def quote(self, ctx, user:discord.Member):
        """Quote a user.
        
        user - The user you wish to quote."""
        logger.info("Quoting a user.")
        async for message in ctx.channel.history():
            if message.author.id == user.id:
                title = f"{user.name} said..."
                embed = discord.Embed(title=title)
                embed.description = message.content
                await ctx.send(embed=embed)
                if len(message.embeds) > 0:
                    for embed in message.embeds:
                        await ctx.send(embed=embed)
                return
        await ctx.send("Could not quote that user.")

    @commands.command()
    async def didsay(self, ctx, user:discord.Member, *phrase):
        """Checks if a user said a particular phrase.
        
        user - A member to mention.
        *phrase - Command checks against this to see what was said."""
        logger.info("Checking if someone said something.")
        quote = " ".join(phrase)
        if len(quote) == 0:
            raise commands.UserInputError("A quote was not specified.")
        async for message in ctx.channel.history():
            if message.author.id == user.id and quote in message.content:
                title = f"Yes, {user.name} said..."
                embed = discord.Embed(title=title)
                embed.description = message.content
                await ctx.send(embed=embed)
                return
        await ctx.send(f"No, {user.name} did not say \"{quote}\". Or it was deleted.")

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Utilities())
