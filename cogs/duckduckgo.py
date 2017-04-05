#!/usr/bin/env python3

"""Contains a cog for stuff that hooks into the DuckDuckGo Instant Answer API."""

# Standard modules
import html
import json
import logging
import urllib.parse

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import errors

# Constants

BASE_URL_DUCKDUCKGO = "https://duckduckgo.com/?%s"

logger = logging.getLogger(__name__)

class Web:
    """This is a cog that contains DuckDuckGo Instant Answers API hooks.
    """
    def __init__(self, bot):
        self.bot = bot
    
    async def _duckduckgo(self, ctx, *query):
        """Retrieve an answer from DuckDuckGo, using the Instant Answers JSON API.
        
        THIS IS NOT A COMMAND AND SHOULD **NOT** BE USED AS A COMMAND. THE REASON IS BECAUSE IT IS
        POTENTIALLY DANGEROUS, AS THE FULL EXTENT OF THE DUCKDUCKGO API IS VERY WIDE.
        """
        if len(query) == 0:
            message = "Query was not specified."
            await ctx.send(message)
            raise commands.UserInputError(message)
        logger.info("Retrieving DuckDuckGo answer with tags %s." % (query,))
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
                await ctx.send(embed=embed)
                logger.info("Answer retrieved!")
            else:
                message = "Failed to fetch. :("
                await ctx.send(message)
                logger.info(message)

    @commands.command()
    async def fortune(self, ctx):
        """Retrieve a random fortune from the Internet."""
        await self._duckduckgo(ctx, "random", "fortune")

    @commands.command(aliases=["randomname"])
    async def rname(self, ctx):
        """Retrieve a random name from the Internet."""
        await self._duckduckgo(ctx, "random", "name")

    @commands.command(aliases=["randint", "randomnumber"])
    async def rng(self, ctx, start:int=1, end:int=100):
        """Retrieve a random number from the Internet.
        
        start - The initial number of the range. Default 1.
        end - The ending number of the range. Default 100."""
        await self._duckduckgo(ctx, "random", "number", str(start), str(end))

def setup(bot):
    """Setup function for Web."""
    bot.add_cog(Web(bot))
