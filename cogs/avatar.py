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
    async def avatar(self, ctx, *, user:discord.Member=None):
        """Display a user's avatar.
        Defaults to displaying the avatar of the user who invoked the command.
        
        user - A member who you can mention for avatar."""
        logger.info("Displaying user avatar.")
        if not user:
            user = ctx.author
        embed = discord.Embed(title=f"The avatar of {user.name}")
        embed.url = user.avatar_url
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Utilities())
