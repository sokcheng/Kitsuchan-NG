#!/usr/bin/env python3

"""This cog contains Arch Linux News functionality."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Constants
BASE_URL_ARCH = "https://www.archlinux.org"
BASE_URL_ARCH_NEWS = "https://www.archlinux.org/news"

class ArchLinux:

    @commands.command(aliases=["anews"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def archnews(self, ctx):
        """Fetch the latest Arch Linux news."""
        async with ctx.bot.session.get(BASE_URL_ARCH_NEWS) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text)
            else:
                await ctx.send("Couldn't fetch Arch Linux news at this time. :<")
                return
        embed = discord.Embed(title="Arch Linux News",
                              url=BASE_URL_ARCH_NEWS,
                              color=0x0F94D2)
        link_list = soup.find_all("a", href=True)
        counter = 0
        for link in link_list:
            if counter == 5:
                break
            elif "/news/" in link['href']:
                post_url = BASE_URL_ARCH + link['href']
                embed.add_field(name=link.string, value=post_url)
                counter += 1
        await ctx.send(embed=embed)

def setup(bot):
    """Setup function for ArchLinux."""
    bot.add_cog(ArchLinux())
