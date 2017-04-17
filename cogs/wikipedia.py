#!/usr/bin/env python3

"""This cog contains a Wikipedia query command."""

# Standard modules
import logging
import urllib.parse

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import errors

logger = logging.getLogger(__name__)

# Constants
BASE_URL_WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php?{0}"

class Web:
    """This cog contains a Wikipedia query command."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["wikipedia"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def wiki(self, ctx, *, query=""):
        """Search Wikipedia.
        
        * *query - A list of strings to be used in the search criteria.
        """
        if len(query) == 0:
            message = "Query not specified."
            raise commands.UserInputError(message)
        logger.info(f"Searching Wikipedia with query {query}.")
        params = urllib.parse.urlencode({"action": "opensearch", "search": query})
        url = BASE_URL_WIKIPEDIA_API.format(params)
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                embed = discord.Embed()
                if len(data) == 0:
                    await ctx.send("Could not find any results. :<")
                    raise errors.ZeroDataLengthError()
                for index in range(0, min(3, len(data[1]))):
                    description = f"{data[3][index]}\n{data[2][index]}"
                    embed.add_field(name=data[1][index], value=description, inline=True)
                await ctx.send(embed=embed)
                logger.info("Data retrieved!")
            else:
                message = "Couldn't reach Wikipedia. x.x"
                await ctx.send(message)
                logger.warning(message)

def setup(bot):
    """Setup function for Wikipedia."""
    bot.add_cog(Web(bot))
