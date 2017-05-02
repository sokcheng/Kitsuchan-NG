#!/usr/bin/env python3

import urllib

import discord
from discord.ext import commands

import kimp
import logging

BASE_URL_KIMP = "https://n303p4.github.io/memes/{0}.html?{1}"

class KIMP:

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def test(self, ctx, image_url:str):
        """A KIMP test."""
        data = kimp.mogrify("test", image_url)
        if data:
            embed = discord.Embed(title="This is a test!")
            embed.description = f"[It's a data URI]({data})"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def standard(self, ctx, top:str, bottom:str, *, member:discord.Member=None):
        """Standard meme. Use quotes around your arguments.
        
        Example usage:
        
        * kit standard \"This is\" "A meme\"
        * kit standard \"This is\" "A meme\" @Kitsuchan"""
        if not member:
            member = ctx.author
        # This is shit.
        url_avatar = member.avatar_url.replace(".webp", ".png")
        params = urllib.parse.urlencode({"image": url_avatar, "top": top,
                                         "bottom": bottom})
        url = BASE_URL_KIMP.format("standard", params)
        embed = discord.Embed(title=f"{member.display_name} as a standard meme!")
        embed.description = f"[Click here to view]({url})"
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function."""
    bot.add_cog(KIMP())
