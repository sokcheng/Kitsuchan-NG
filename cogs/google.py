#!/usr/bin/env python3

"""This cog contains Google functionality. It is AWFUL."""

# Standard modules
import json
import logging
import random
import re

# Third-party modules
from bs4 import BeautifulSoup
from discord.ext import commands

systemrandom = random.SystemRandom()

logger = logging.getLogger(__name__)

# Constants
BASE_URL_GOOGLE = "https://www.google.com/search?q={0}"
BASE_URL_GOOGLE_IMAGES = "https://www.google.com/search?q={0}&tbm=isch"
BASE_URL_GOOGLE_NEWS = "https://www.google.com/search?q={0}&tbm=nws"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"
HEADERS = {"User-Agent": USER_AGENT}

PATTERN_URL_START = "^http(s)://"

class Google:

    async def _google(self, ctx, *, query:str, base_url=BASE_URL_GOOGLE):
        """Helper function for Google.
        
        * query - The search query desired.
        * base_url - The Google base URL we want."""
        url = base_url.format(query)
        async with ctx.bot.session.request("GET", url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.text()
                soup = BeautifulSoup(data)
                if base_url == BASE_URL_GOOGLE:
                    links = soup.find_all("cite", class_="_Rm")
                    for index in range(len(links)):
                        full_link = []
                        for content in links[index].contents:
                            content = str(content).replace("<b>", "").replace("</b>", "")
                            full_link.append(content)
                        full_link = "".join(full_link)
                        if not re.match(PATTERN_URL_START, full_link):
                            full_link = "http://" + full_link
                        links[index] = full_link
                    return links
                elif base_url == BASE_URL_GOOGLE_IMAGES:
                    links = soup.find_all("div", class_="rg_meta")
                    for index in range(len(links)):
                        links[index] = json.loads(links[index].contents[0]).get("ou")
                    return links
                elif base_url == BASE_URL_GOOGLE_NEWS:
                    links = soup.find_all("a", class_="l _HId")
                    for index in range(len(links)):
                        links[index] = links[index]["href"]
                    return links
            else:
                message = "Could not reach Google. x.x"
                return message
    
    @commands.group(aliases=["g"], invoke_without_command=True)
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def google(self, ctx, *, query:str):
        """Search Google. Optional image and news arguments.
        
        Example queries:
        
        * google A cat - Search Google for a cat.
        * google image A cat - Search Google for an image of a cat."""
        links = await self._google(ctx, query=query)
        if isinstance(links, list):
            see_also = [f"<{link}>" for link in links[1:4]]
            see_also = "\n".join(see_also)
            message = f"{links[0]}\n\n**You may also want to look at:**\n{see_also}"
            await ctx.send(message)
        else:
            await ctx.send(links)
            logger.warning(links)

    @google.command(aliases=["i"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def image(self, ctx, *, query:str):
        """Search Google Images."""
        links = await self._google(ctx, query=query, base_url=BASE_URL_GOOGLE_IMAGES)
        if isinstance(links, list):
            link = systemrandom.choice(links)
            await ctx.send(link)
        else:
            await ctx.send(links)
            logger.warning(links)

    @google.command(aliases=["n"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def news(self, ctx, *, query:str):
        """Search Google News."""
        links = await self._google(ctx, query=query, base_url=BASE_URL_GOOGLE_NEWS)
        if isinstance(links, list):
            see_also = [f"<{link}>" for link in links[1:4]]
            see_also = "\n".join(see_also)
            message = f"{links[0]}\n\n**You may also want to look at:**\n{see_also}"
            await ctx.send(message)
        else:
            await ctx.send(links)
            logger.warning(links)

def setup(bot):
    """Setup function for Google."""
    bot.add_cog(Google())
