#!/usr/bin/env python3

"""This cog contains a dictionary lookup command."""

# Standard modules
import logging
import re
import urllib.parse

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import errors

logger = logging.getLogger(__name__)

# Constants
BASE_URL_OWL_API = "https://owlbot.info/api/v1/dictionary/{0}{1}"

MAX_NUM_RESULTS = 5

class Dictionary:
    """Dictionary command."""

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def define(self, ctx, *, word=""):
        """Define a word
        
        * word - A word to be looked up.
        """
        if len(word) == 0:
            message = "Word not specified."
            raise commands.UserInputError(message)
        word = word.lower()
        params = "?{0}".format(urllib.parse.urlencode({"format": "json"}))
        url = BASE_URL_OWL_API.format(word, params)
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if len(data) == 0:
                    await ctx.send("Could not find any results. :<")
                    raise errors.ZeroDataLengthError()
                embed = discord.Embed(title=word)
                embed.url = BASE_URL_OWL_API.format(word, "")
                for index in range(0, min(MAX_NUM_RESULTS, len(data))):
                    result = data[index]
                    definition = re.sub("<.*?>|\u00E2|\u0080|\u0090", "",
                                        result['defenition'].capitalize())
                    example = re.sub("<.*?>|\u00E2|\u0080|\u0090", "",
                                     result['example'].capitalize())
                    description = f"{definition}\nExample: *{example}*"
                    embed.add_field(name=result["type"], value=description)
                if len(data) > MAX_NUM_RESULTS:
                    embed.set_footer(text=f"...and {len(data)-MAX_NUM_RESULTS} other result(s)")
                await ctx.send(embed=embed)
                logger.info("Data retrieved!")
            else:
                message = "Something broke. x.x"
                await ctx.send(message)
                logger.warning(message)

def setup(bot):
    """Setup function for Wikipedia."""
    bot.add_cog(Dictionary())
