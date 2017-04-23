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
import checks
import errors
import settings

logger = logging.getLogger(__name__)

# Constants
BASE_URL_IBSEARCH_API = "https://ibsear.ch/api/v1/images.json?{0}"
BASE_URL_IBSEARCH_IMAGE = "https://{0[server]}.ibsear.ch/{0[path]}"

class IbSearch:
    """IbSear.ch command."""
    def __init__(self):
        self.key_ibsearch = settings.manager.get("API_KEY_IBSEARCH")

    @commands.command(aliases=["ib", "ibs"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def ibsearch(self, ctx, *, tags=""):
        """Fetch a randomized anime image from IbSear.ch, optional tags.
        
        * tags - A list of tags to be used in the search criteria.
        
        This command accepts common imageboard tags and keywords. Here are a few examples:
        
        * ib red_hair armor - Search for images tagged with `red_hair` and `armor`.
        * ib red_hair -armor - Search for images tagged with `red_hair` and not `armor`.
        * ib 1280x1024 - Search for images that are 1280x1024.
        * ib 5:4 - Search for images in 5:4 aspect ratio.
        * ib random: - You don't care about what you get.
        """
        if not self.key_ibsearch:
            message = "API key required for this command, but none found. Contact the bot owner?"
            await ctx.send(message)
            raise errors.KeyError(message)
        logger.info(f"Fetching image with tags {tags}.")
        params = urllib.parse.urlencode({"key": self.key_ibsearch, "q": tags})
        url = BASE_URL_IBSEARCH_API.format(params)
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if len(data) == 0:
                    await ctx.send("Could not find any results. :<")
                    raise errors.ZeroDataLengthError()
                index = random.randint(1, len(data)) - 1
                result = data[index]
                url_image = BASE_URL_IBSEARCH_IMAGE.format(result)
                if ctx.guild and ctx.guild.explicit_content_filter.name == "disabled":
                    embed = discord.Embed(title="Click here for full image")
                    embed.url = url_image
                    embed.set_image(url=url_image)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(url_image)
                    logger.info("Image retrieved!")
            else:
                message = "Could not reach IbSear.ch. x.x"
                await ctx.send(message)
                logger.warning(message)

def setup(bot):
    """Setup function for Web."""
    bot.add_cog(IbSearch())
