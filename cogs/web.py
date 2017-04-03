#!/usr/bin/env python3

"""Contains a cog for stuff that hooks into web APIs."""

# Standard modules
import html
import json
import logging
import random
import re
import urllib.parse

# Third-party modules
import aiohttp
import discord
from discord.ext import commands

# Bundled modules
import settings
import errors
import utils

# Constants

BASE_URL_IBSEARCH = "https://ibsear.ch/api/v1/images.json?%s"
BASE_URL_IBSEARCH_IMAGE = "https://%s.ibsear.ch/%s"
BASE_URL_IBSEARCH_XXX = "https://ibsearch.xxx/api/v1/images.json?%s"
BASE_URL_IBSEARCH_XXX_IMAGE = "https://%s.ibsearch.xxx/%s"

BASE_URL_WIKIPEDIA = "https://en.wikipedia.org/w/api.php?%s"

BASE_URL_XKCD = "https://xkcd.com/%s/"
BASE_URL_XKCD_API = "https://xkcd.com/%s/info.0.json"

logger = logging.getLogger(__name__)

def setup(bot):
    """Setup function for Web."""
    bot.add_cog(Web(bot, logger))

class Web:
    """This is a cog that contains Web API hooks.
    """
    def __init__(self, bot, logger):
        self.name = "Web APIs"
        self.bot = bot
        self.key_ibsearch = settings.manager.get("API_KEY_IBSEARCH")
        self.logger = logger

    @commands.command(brief="Search Wikipedia.", aliases=["wikipedia"])
    async def wiki(self, ctx, *query):
        """Search Wikipedia.
        
        *query - A list of strings to be used in the search criteria.
        """
        if len(query) == 0:
            message = "Please enter a query."
            await ctx.send(message)
            raise errors.InputError("", message)
        self.logger.info("Searching Wikipedia with query %s." % (query,))
        query_search = " ".join(query)
        params = urllib.parse.urlencode({"action": "opensearch", "search": query_search})
        url = BASE_URL_WIKIPEDIA % params
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if len(data) == 0:
                    await ctx.send("Could not find any results.")
                    raise errors.ZeroDataLengthError()
                for index in range(0, min(3, len(data[1]))):
                    embed = discord.Embed(title=data[1][index], url=data[3][index])
                    embed.description = data[2][index]
                    await ctx.send(embed=embed)
                self.logger.info("Data retrieved!")
            else:
                message = "Failed to reach Wikipedia. :("
                await ctx.send(message)
                self.logger.info(message)

    @commands.command(brief="Fetch an anime image from IbSear.ch.", aliases=["ib"])
    async def ibsearch(self, ctx, *tags):
        """Fetch a randomized anime image from IbSear.ch.
        
        *tags - A list of tag strings to be used in the search criteria.
        
        This command accepts common imageboard tags and keywords. Here are a few examples:
        
        >> ib red_hair armor - Search for images tagged with either red_hair or armor.
        >> ib +animal_ears +armor - Search for images tagged with both red_hair and armor.
        >> ib 1280x1024 - Search for images that are 1920x1080.
        >> ib 5:4 - Search for images in 5:4 aspect ratio.
        >> ib random: - You don't care about what you get."""
        if not self.key_ibsearch:
            message = "API key not specified! Command halted."
            await ctx.send(message)
            raise errors.KeyError(message)
        self.logger.info("Fetching image with tags %s." % (tags,))
        hash_id_channel = utils.to_hash(str(ctx.channel.id))
        settings.manager.setdefault("WHITELIST_NSFW", [])
        if hash_id_channel in settings.manager["WHITELIST_NSFW"]:
            self.logger.info("NSFW allowed for channel %s." % (ctx.channel.id,))
            base_url = BASE_URL_IBSEARCH_XXX
            base_url_image = BASE_URL_IBSEARCH_XXX_IMAGE
        else:
            self.logger.info("NSFW disallowed for channel %s." % (ctx.channel.id,))
            base_url = BASE_URL_IBSEARCH
            base_url_image = BASE_URL_IBSEARCH_IMAGE
        query_tags = " ".join(tags)
        params = urllib.parse.urlencode({"key": self.key_ibsearch, "q": query_tags})
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
