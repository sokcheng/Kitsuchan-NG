#!/usr/bin/env python3

"""Contains a cog that fetches user avatars."""

# Standard modules
import logging

# Third party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Avatar:
    """Avatar command."""
    
    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def avatar(self, ctx, *, user:discord.Member=None):
        """Display a user's avatar.
        Defaults to displaying the avatar of the user who invoked the command.
        
        * user - A member who you can mention for avatar."""
        if not user:
            user = ctx.author
        if ctx.guild and ctx.guild.explicit_content_filter.name == "disabled":
            embed = discord.Embed()
            embed.url = user.avatar_url
            embed.set_image(url=user.avatar_url)
            embed.set_footer(text=f"Avatar for {user.name}")
            await ctx.send(embed=embed)
        else:
            await ctx.send(user.avatar_url)

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Avatar())
