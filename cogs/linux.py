#!/usr/bin/env python3

"""This cog contains Linux news functionality."""

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

BASE_URL_OMGUBUNTU = "http://www.omgubuntu.co.uk/"

BASE_URL_FEDORA_MAGAZINE = "https://fedoramagazine.org/"

class Linux:

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

    async def _generic_news(self, ctx, base_url:str, title:str="News", color:int=None):
        async with ctx.bot.session.get(base_url) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text)
            else:
                await ctx.send("Couldn't fetch Ubuntu Linux news at this time. :<")
                return
        embed = discord.Embed(title=title,
                              url=base_url,
                              color=color)
        link_list = soup.find_all("a", href=True, rel="bookmark")
        counter = 0
        checked_links = []
        for link in link_list:
            if counter == 5:
                break
            elif link['href'] not in checked_links and link.string:
                embed.add_field(name=link.string, value=link['href'])
                checked_links.append(link['href'])
                counter += 1
        await ctx.send(embed=embed)

    @commands.command(aliases=["unews"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def ubuntunews(self, ctx):
        """Fetch the latest Ubuntu Linux news."""
        await self._generic_news(ctx, BASE_URL_OMGUBUNTU, "Ubuntu News", 0x5E2750)

    @commands.command(aliases=["fnews"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def fedoranews(self, ctx):
        """Fetch the latest Fedora Linux news."""
        await self._generic_news(ctx, BASE_URL_FEDORA_MAGAZINE, "Fedora News", 0x3C6DB4)

def setup(bot):
    """Setup function for Linux."""
    bot.add_cog(Linux())