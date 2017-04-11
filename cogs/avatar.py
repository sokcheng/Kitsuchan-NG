#!/usr/bin/env python3

"""Contains a cog that fetches user avatars."""

# Standard modules
import logging

# Third party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Utilities:
    """discord.py cog containing avatar fetcher."""
    
    def __init__(self):
        pass
    
    @commands.command()
    async def avatar(self, ctx, *, user:discord.Member=None):
        """Display a user's avatar.
        Defaults to displaying the avatar of the user who invoked the command.
        
        * user - A member who you can mention for avatar."""
        logger.info("Displaying user avatar.")
        if not user:
            user = ctx.author
        embed = discord.Embed()
        embed.url = user.avatar_url
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text=f"The avatar of {user.name}")
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Utilities())
