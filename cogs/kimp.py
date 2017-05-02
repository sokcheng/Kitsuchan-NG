#!/usr/bin/env python3

import urllib

import discord
from discord.ext import commands

import logging

BASE_URL_KIMP = "https://n303p4.github.io/{0}.html?{1}"

class KIMP:

    def mogrify(self, template:str, **kwargs):
        """Meme generation.
        
        * template - The name of the template to use.
        * **args - The arguments to use in the format.
        """
        params = urllib.parse.urlencode(kwargs)
        url = BASE_URL_KIMP.format(template, params)
        return url

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def standard(self, ctx, top:str, bottom:str, *, member:discord.Member=None):
        """Standard meme. Use quotes around your arguments.
        
        Example usage:
        
        * kit standard \"This is\" "A meme\"
        * kit standard \"This is\" "A meme\" @Kitsuchan"""
        if not member:
            member = ctx.author
        url_avatar = member.avatar_url.replace(".webp", ".png")
        url = self.mogrify("standard", image=url_avatar, top=top, bottom=bottom)
        embed = discord.Embed(title=f"{member.display_name} as a standard meme!")
        embed.description = f"[Click here to view]({url})"
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function."""
    bot.add_cog(KIMP())
