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
BASE_URL_XKCD = "https://xkcd.com/{0}/"
BASE_URL_XKCD_API = "https://xkcd.com/{0}/info.0.json"
BASE_URL_XKCD_EXPLAIN = "http://www.explainxkcd.com/wiki/index.php/{0}"

class Web:
    """This cog contains some basic xkcd commands."""

    async def _xkcd(self, ctx, comic_id=""):
        """Helper function for xkcd comics."""
        logger.info(f"Retrieving xkcd comic with ID {comic_id}.")
        if comic_id.lower() in ("random", "r"):
            url = BASE_URL_XKCD_API.format("")
            async with ctx.bot.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    comic_id = random.randint(1, data["num"])
                else:
                    message = "Could not reach xkcd. x.x"
                    await ctx.send(message)
                    logger.info(message)
                    return
        url = BASE_URL_XKCD_API.format(comic_id)
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                title = data["safe_title"]
                url = BASE_URL_XKCD.format(data["num"])
                url_explanation = BASE_URL_XKCD_EXPLAIN.format(data["num"])
                url_image = data["img"]
                alt = data.get('alt')
                if ctx.guild and ctx.guild.explicit_content_filter.name == "disabled":
                    embed = discord.Embed(title=f'{title} ({data["num"]})')
                    embed.description = f"[Explanation]({url_explanation})"
                    embed.url = url
                    embed.set_image(url=url_image)
                    if alt:
                        embed.set_footer(text=alt)
                    await ctx.send(embed=embed)
                else:
                    message_fetching = await ctx.send("Fetching image; please wait. :3")
                    message = [f"**{title}**",
                               f"**URL:** <{url}>",
                               f"**Explanation:** <{url_explanation}>",
                               f"**Image URL:** {url_image}",
                               alt]
                    message = "\n".join(message)
                    await ctx.send(message)
                    await message_fetching.delete()
            elif response.status == 404:
                message = "That comic doesn't exist. :<"
                await ctx.send(message)
                logger.info(message)
            else:
                message = "Could not reach xkcd. x.x"
                await ctx.send(message)
                logger.warning(message)

    @commands.command(aliases=["xk"])
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def xkcd(self, ctx, comic_id=""):
        """Fetch a comic from xkcd.
        
        * comic_id - A desired comic ID. Leave blank for latest comic. Set to r for a random comic.
        """
        await self._xkcd(ctx, comic_id)

    @commands.command(hidden=True)
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def antigravity(self, ctx):
        """Fetch the antigravity comic from xkcd."""
        await self._xkcd(ctx, "353")

    @commands.command(hidden=True)
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def sudo(self, ctx):
        """Fetch the sudo comic from xkcd."""
        await self._xkcd(ctx, "149")

def setup(bot):
    """Setup function for xkcd."""
    bot.add_cog(Web())
