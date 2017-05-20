#!/usr/bin/env python3

"""This cog contains Linux news functionality."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands
from bs4 import BeautifulSoup

# Bundled modules
import helpers

logger = logging.getLogger(__name__)

# Constants
BASE_URL_ARCH = "https://www.archlinux.org"
BASE_URL_ARCH_NEWS = "https://www.archlinux.org/news"

BASE_URL_OMGUBUNTU = "http://www.omgubuntu.co.uk/"
IMAGE_URL_OMGUBUNTU = ("http://www.omgubuntu.co.uk/wp-content/themes/"
                       "omgubuntu-theme-3.6.1/images/logo.png")

BASE_URL_FEDORA_MAGAZINE = "https://fedoramagazine.org/"

BASE_URL_ANTERGOS_NEWS = "https://antergos.com/news/"
IMAGE_URL_ANTERGOS = "https://avatars2.githubusercontent.com/u/4215718?v=3&s=128"

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
        embed = discord.Embed(title="Arch Linux News", url=BASE_URL_ARCH_NEWS, color=0x0F94D2)
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

    async def _generic_news(self, ctx, base_url:str, *, title:str="News", image_url:str=None,
                            color:int=None, no_link_titles:bool=False, **attributes):
        async with ctx.bot.session.get(base_url) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text)
            else:
                await ctx.send(f"Couldn't fetch {title} at this time. :<")
                return
        embed = discord.Embed(title=title, url=base_url, color=color)
        if image_url:
            if not helpers.has_scanning(ctx):
                embed.set_thumbnail(url=image_url)
            else:
                embed.set_footer(text="Thumbnail omitted on this channel due to image scanning.")
        link_list = soup.find_all("a", href=True, **attributes)
        counter = 0
        checked_links = []
        if no_link_titles:
            description = []
            for link in link_list:
                if counter == 5:
                    break
                elif link['href'] not in checked_links and link.string:
                    description.append(link['href'])
                    counter += 1
            description = "\n".join(description)
            embed.description = description
        else:
            for link in link_list:
                if counter == 5:
                    break
                elif link['href'] not in checked_links and link.string:
                    embed.add_field(name=link.string, value=link['href'])
                    checked_links.append(link['href'])
                    counter += 1
        await ctx.send(embed=embed)

    @commands.command(aliases=["unews", "omgubuntu"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def ubuntunews(self, ctx):
        """Fetch the latest Ubuntu Linux news."""
        await self._generic_news(ctx, BASE_URL_OMGUBUNTU, title="OMG! Ubuntu!",
                                 image_url=IMAGE_URL_OMGUBUNTU, color=0x5E2750,
                                 rel="bookmark")

    @commands.command(aliases=["fnews"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def fedoranews(self, ctx):
        """Fetch the latest Fedora Linux news."""
        await self._generic_news(ctx, BASE_URL_FEDORA_MAGAZINE, title="Fedora News",
                                 color=0x263D6A, rel="bookmark")

    @commands.command(aliases=["annews"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def antergosnews(self, ctx):
        """Fetch the latest Antergos news."""
        await self._generic_news(ctx, BASE_URL_ANTERGOS_NEWS, title="Antergos News",
                                 image_url=IMAGE_URL_ANTERGOS, color=0x7D97C4,
                                 no_link_titles=True, class_="more-link")

def setup(bot):
    """Setup function for Linux."""
    bot.add_cog(Linux())
