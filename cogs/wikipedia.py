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

# Constants

BASE_URL_WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php?%s"

logger = logging.getLogger(__name__)

class Web:
    """This cog contains a Wikipedia query command."""
    def __init__(self, bot):
        self.name = "Web APIs"
        self.bot = bot

    @commands.command(aliases=["wikipedia"])
    async def wiki(self, ctx, *query):
        """Search Wikipedia.
        
        * *query - A list of strings to be used in the search criteria.
        """
        if len(query) == 0:
            message = "Query not specified."
            raise commands.UserInputError(message)
        logger.info(f"Searching Wikipedia with query {query}.")
        query_search = " ".join(query)
        params = urllib.parse.urlencode({"action": "opensearch", "search": query_search})
        url = BASE_URL_WIKIPEDIA_API % params
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                embed = discord.Embed()
                if len(data) == 0:
                    await ctx.send("Could not find any results.")
                    raise errors.ZeroDataLengthError()
                for index in range(0, min(3, len(data[1]))):
                    description = f"{data[3][index]}\n{data[2][index]}"
                    embed.add_field(name=data[1][index], value=description, inline=True)
                await ctx.send(embed=embed)
                logger.info("Data retrieved!")
            else:
                message = "Failed to reach Wikipedia. :("
                await ctx.send(message)
                logger.info(message)

def setup(bot):
    """Setup function for Web."""
    bot.add_cog(Web(bot))
