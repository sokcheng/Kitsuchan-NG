#!/usr/bin/env python3

import urllib

import discord
from discord.ext import commands

import logging

BASE_URL_MEME = "https://n303p4.github.io/{0}.html?{1}"

class Memes:

    def mogrify(self, template:str, **kwargs):
        """Meme generation.
        
        * template - The name of the template to use.
        * **args - The arguments to use in the format.
        """
        params = urllib.parse.urlencode(kwargs)
        url = BASE_URL_MEME.format(template, params)
        return url

    @commands.command(aliases=["um", "standard"])
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def usermeme(self, ctx, top:str, bottom:str, *, member:discord.Member=None):
        """Create a meme of a user. Use quotes around your arguments.
        
        Example usage:
        
        * kit usermeme \"This is\" "A meme\"
        * kit usermeme \"This is\" "A meme\" @Kitsuchan
        """
        if not member:
            member = ctx.author
        url_avatar = member.avatar_url.replace(".webp", ".png")
        url = self.mogrify("standard", title=" / ".join((top, bottom)),
                           image=url_avatar, top=top, bottom=bottom)
        embed = discord.Embed(title=f"{member.display_name} as a standard meme!")
        embed.description = f"[Click here to view]({url})"
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function."""
    bot.add_cog(Memes())
