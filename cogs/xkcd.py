#!/usr/bin/env python3

"""This cog contains some basic xkcd commands."""

# Standard modules
import logging
import random

# Third-party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

# Constants
BASE_URL_XKCD = "https://xkcd.com/%s/"
BASE_URL_XKCD_API = "https://xkcd.com/%s/info.0.json"
BASE_URL_XKCD_EXPLAIN = "http://www.explainxkcd.com/wiki/index.php/%s"

class Web:
    """This cog contains some basic xkcd commands."""
    def __init__(self, bot):
        self.bot = bot

    async def _xkcd(self, ctx, comic_id=""):
        """Helper function for xkcd comics."""
        logger.info(f"Retrieving xkcd comic with ID {comic_id}.")
        if comic_id.lower() in ("random", "r"):
            url = BASE_URL_XKCD_API % ("",)
            async with self.bot.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    comic_id = random.randint(1, data["num"])
                else:
                    message = "Could not reach xkcd. :("
                    await ctx.send(message)
                    logger.info(message)
                    return
        url = BASE_URL_XKCD_API % (comic_id,)
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                title = data["safe_title"]
                embed = discord.Embed(title=f"{title} ({data['num']})")
                url_explanation = BASE_URL_XKCD_EXPLAIN % (comic_id,)
                embed.description = f"[Explanation]({url_explanation})"
                embed.url = BASE_URL_XKCD % (comic_id,)
                if data.get('alt'):
                    embed.set_footer(text=data['alt'])
                embed.set_image(url=data["img"])
                await ctx.send(embed=embed)
            elif response.status == 404:
                message = "That comic doesn't exist."
                await ctx.send(message)
                logger.info(message)
            else:
                message = "Could not reach xkcd. :("
                await ctx.send(message)
                logger.info(message)

    @commands.command(aliases=["xk"])
    async def xkcd(self, ctx, comic_id=""):
        """Fetch a comic from xkcd.
        
        * comic_id - A desired comic ID. Leave blank for latest comic. Set to r for a random comic.
        """
        await self._xkcd(ctx, comic_id)

    @commands.command(hidden=True)
    async def antigravity(self, ctx):
        """Fetch the antigravity comic from xkcd."""
        await self._xkcd(ctx, "353")

    @commands.command(hidden=True)
    async def sudo(self, ctx):
        """Fetch the sudo comic from xkcd."""
        await self._xkcd(ctx, "149")

def setup(bot):
    """Setup function for xkcd."""
    bot.add_cog(Web(bot))
