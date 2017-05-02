#!/usr/bin/env python3

import kimp
import logging

import discord
from discord.ext import commands

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
    async def standard(self, ctx, *args):
        """Standard meme. Use quotes around your arguments.
        
        Example usage:
        
        * kit standard \"This is\" "A meme\""""
        if len(args) < 2:
            raise commands.UserInputError("Need a top and a bottom phrase!")
        # This is shit.
        data = kimp.mogrify("standard", ctx.author.avatar_url.replace(".webp", ".png"), *args)
        if data:
            embed = discord.Embed(title="This is a test!")
            embed.description = f"[It's a data URI]({data})"
            await ctx.send(embed=embed)

def setup(bot):
    """Setup function."""
    bot.add_cog(KIMP())
