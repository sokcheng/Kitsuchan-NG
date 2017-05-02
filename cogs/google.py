#!/usr/bin/env python3

"""This cog contains some basic xkcd commands."""

# Standard modules
import logging
import random
import re

# Third-party modules
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

# Bundled modules
import helpers

logger = logging.getLogger(__name__)

# Constants
BASE_URL_GOOGLE = "https://www.google.com/search?q={0}"
BASE_URL_GOOGLE_IMAGES = "https://www.google.com/search?q={0}&tbm=isch"

USER_AGENT = "NetSurf/3.6 (Linux, Ubuntu)"
HEADERS = {"User-Agent": USER_AGENT}

PATTERN_URL_START = "^http(s)://"

class Google:
    """xkcd command."""

    async def _google(self, ctx, *, query:str, base_url=BASE_URL_GOOGLE):
        """Helper function for Google.
        
        * query - The search query desired.
        * base_url - The Google base URL we want."""
        url = base_url.format(query)
        async with ctx.bot.session.request("GET", url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.text()
                soup = BeautifulSoup(data)
                links = soup.find_all("cite", class_=None)
                for index in range(len(links)):
                    full_link = []
                    for content in links[index].contents:
                        content = str(content).replace("<b>", "").replace("</b>", "")
                        full_link.append(content)
                    full_link = "".join(full_link)
                    if not re.match(PATTERN_URL_START, full_link):
                        full_link = "http://" + full_link
                    links[index] = full_link
                see_also = [f"<{link}>" for link in links[1:4]]
                see_also = "\n".join(see_also)
                message = f"{links[0]}\n\n**You may also want to look at:**\n{see_also}"
                await ctx.send(message)
            else:
                message = "Could not reach Google. x.x"
                await ctx.send(message)
                logger.warning(message)
    
    @commands.group(aliases=["g"], invoke_without_command=True)
    async def google(self, ctx, *, query:str):
        await self._google(ctx, query=query)

    @google.command(aliases=["i"])
    async def image(self, ctx, *, query:str,):
        await self._google(ctx, query=query, base_url=BASE_URL_GOOGLE_IMAGES)

def setup(bot):
    """Setup function for Google."""
    bot.add_cog(Google())
