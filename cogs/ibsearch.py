#!/usr/bin/env python3

"""This cog handles IbSear.ch queries."""

# Standard modules
import logging
import random
import urllib.parse

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import settings
import errors
import utils

# Constants

BASE_URL_IBSEARCH_API = "https://ibsear.ch/api/v1/images.json?%s"
BASE_URL_IBSEARCH_IMAGE = "https://%s.ibsear.ch/%s"
BASE_URL_IBSEARCH_XXX_API = "https://ibsearch.xxx/api/v1/images.json?%s"
BASE_URL_IBSEARCH_XXX_IMAGE = "https://%s.ibsearch.xxx/%s"

logger = logging.getLogger(__name__)

class Web:
    """This cog handles IbSear.ch queries."""
    def __init__(self, bot):
        self.name = "Web APIs"
        self.bot = bot
        self.key_ibsearch = settings.manager.get("API_KEY_IBSEARCH")

    @commands.command(aliases=["ib"])
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
        logger.info(f"Fetching image with tags {tags}.")
        hash_id_channel = utils.to_hash(str(ctx.channel.id))
        settings.manager.setdefault("WHITELIST_NSFW", [])
        if hash_id_channel in settings.manager["WHITELIST_NSFW"]:
            logger.info(f"NSFW allowed for channel {ctx.channel.id}.")
            base_url_api = BASE_URL_IBSEARCH_XXX_API
            base_url_image = BASE_URL_IBSEARCH_XXX_IMAGE
        else:
            logger.info(f"NSFW disallowed for channel {ctx.channel.id}.")
            base_url_api = BASE_URL_IBSEARCH_API
            base_url_image = BASE_URL_IBSEARCH_IMAGE
        query_tags = " ".join(tags)
        params = urllib.parse.urlencode({"key": self.key_ibsearch, "q": query_tags})
        url = base_url_api % params
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
                logger.info("Image retrieved!")
            else:
                message = "Failed to fetch image. :("
                await ctx.send(message)
                logger.info(message)

def setup(bot):
    """Setup function for Web."""
    bot.add_cog(Web(bot))
