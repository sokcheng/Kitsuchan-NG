#!/usr/bin/env python3

"""Contains a cog for stuff that hooks into web APIs."""

# Standard modules
import html
import json
import random
import urllib.parse

# Third-party modules
import aiohttp
import asyncio
import discord
from discord.ext import commands

# Bundled modules
import errors
from environment import *

# Constants

BASE_URL_DUCKDUCKGO = "https://duckduckgo.com/?%s"

BASE_URL_IBSEARCH = "https://ibsear.ch/api/v1/images.json?%s"
BASE_URL_IBSEARCH_IMAGE = "https://%s.ibsear.ch/%s"
BASE_URL_IBSEARCH_XXX = "https://ibsearch.xxx/api/v1/images.json?%s"
BASE_URL_IBSEARCH_XXX_IMAGE = "https://%s.ibsearch.xxx/%s"

BASE_URL_XKCD = "https://xkcd.com/%s/"
BASE_URL_XKCD_API = "https://xkcd.com/%s/info.0.json"

class APIs:
    """This is a cog that contains Web API hooks.
    """
    def __init__(self, bot, logger, api_key_ibsearch):
        self.bot = bot
        self.logger = logger
        self.api_key_ibsearch = api_key_ibsearch
    
    @commands.command(brief="Retrieve an answer from DuckDuckGo.", aliases=["ddg"])
    async def duckduckgo(self, ctx, *query):
        """Retrieve an answer from DuckDuckGo, using the Instant Answers JSON API.
        
        *query - A list of strings to be used in the search criteria.
        
        This command is extremely versatile! Here are a few examples of things you can do with it:
        
        >> ddg roll 5d6 - Roll five 6-sided dice.
        >> ddg 40 f in c - Convert 40 degrees Fahrenheit to Celsius.
        >> ddg (5+6)^2/4 - Produces 30.25.
        >> ddg random number 1 100 - Generate a random number from 1 to 100.
        >> ddg random name - Generate a random name.
        >> ddg random fortune - Generate a random fortune.
        """
        self.logger.info("Retrieving DuckDuckGo answer with tags %s." % (query,))
        query_search = " ".join(query)
        params = urllib.parse.urlencode({"q": query_search, "t": "ffsb",
                                         "format": "json", "ia": "answer"})
        url = BASE_URL_DUCKDUCKGO % params
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                # This should be response.json() directly, but DuckDuckGo returns an incorrect MIME.
                data = await response.text()
                data = json.loads(data)
                if len(data) == 0:
                    # I wanted to put statements like this in on_command_error.
                    # However, it seems not to work when the ctx.send is in an elif block. :/
                    await ctx.send("Could not find any results.")
                    raise errors.ZeroDataLengthError()
                answer = html.unescape(data["Answer"])
                embed = discord.Embed(title=answer)
                params_short = urllib.parse.urlencode({"q": query_search})
                embed.description = BASE_URL_DUCKDUCKGO % params_short
                await ctx.send(embed=embed)
                self.logger.info("Answer retrieved!")
            else:
                message = "Failed to fetch answer. :("
                await ctx.send(message)
                self.logger.info(message)

    @commands.command(brief="Fetch an image from IbSear.ch.", aliases=["ib"])
    async def ibsearch(self, ctx, *tags):
        """Retrieve a randomized image from IbSear.ch.
        
        *tags - A list of tag strings to be used in the search criteria.
        
        This command accepts common imageboard tags and keywords. Here are a few examples:
        
        >> ib red_hair armor - Search for images tagged with either red_hair or armor.
        >> ib +animal_ears +armor - Search for images tagged with both red_hair and armor.
        >> ib 1280x1024 - Search for images that are 1920x1080.
        >> ib 5:4 - Search for images in 5:4 aspect ratio.
        >> ib random: - You don't care about what you get."""
        self.logger.info("Fetching image with tags %s." % (tags,))
        if str(ctx.channel.id) in WHITELIST_NSFW:
            self.logger.info("NSFW allowed for channel %s." % (ctx.channel.id,))
            base_url = BASE_URL_IBSEARCH_XXX
            base_url_image = BASE_URL_IBSEARCH_XXX_IMAGE
        else:
            self.logger.info("NSFW disallowed for channel %s." % (ctx.channel.id,))
            base_url = BASE_URL_IBSEARCH
            base_url_image = BASE_URL_IBSEARCH_IMAGE
        query_tags = " ".join(tags)
        params = urllib.parse.urlencode({"key": API_KEY_IBSEARCH, "q": query_tags})
        url = base_url % params
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if len(data) == 0:
                    await ctx.send("Could not find any results.")
                    raise errors.ZeroDataLengthError()
                index = random.randint(1, len(data)) - 1
                result = data[index]
                embed = discord.Embed()
                url_image = base_url_image % (data[index]["server"], data[index]["path"])
                embed.description = url_image
                embed.set_image(url=url_image)
                await ctx.send(embed=embed)
                self.logger.info("Image retrieved!")
            else:
                message = "Failed to fetch image. :("
                await ctx.send(message)
                self.logger.info(message)

    @commands.command(brief="Fetch a comic from xkcd.", aliases=["xk"])
    async def xkcd(self, ctx, comic_id=""):
        """Retrieve a comic from xkcd.
        
        comic_id - A desired comic ID. Leave blank for latest comic. Set to r for a random comic.
        """
        self.logger.info("Retrieving xkcd comic with ID %s." % (comic_id,))
        if comic_id.lower() in ("random", "r"):
            url = BASE_URL_XKCD_API % ("",)
            async with self.bot.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    comic_id = random.randint(1, data["num"])
                else:
                    message = "Could not reach xkcd. :("
                    await ctx.send(message)
                    self.logger.info(message)
                    return
        url = BASE_URL_XKCD_API % (comic_id,)
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                title = data["safe_title"]
                embed = discord.Embed(title=title)
                embed.description = "%s\n%s" % (BASE_URL_XKCD % comic_id, data.get("alt"),)
                embed.set_image(url=data["img"])
                await ctx.send(embed=embed)
            elif response.status == 404:
                message = "That comic doesn't exist."
                await ctx.send(message)
                self.logger.info(message)
            else:
                message = "Could not reach xkcd. :("
                await ctx.send(message)
                self.logger.info(message)
