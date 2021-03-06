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
    async def define(self, ctx, word:str):
        """Define a word.
        
        * word - A word to be looked up.
        """
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
                
                results_to_display = min(MAX_NUM_RESULTS, len(data))
                
                for index in range(0, results_to_display):
                    result = data[index]
                    definition = result.get('defenition')
                    description = re.sub("<.*?>|\u00E2|\u0080|\u0090", "",
                                         definition.capitalize())
                    example = result.get('example')
                    if example:
                        example = re.sub("<.*?>|\u00E2|\u0080|\u0090", "",
                                         example.capitalize())
                        description = f"{description}\nExample: *{example}*"
                    embed.add_field(name=result["type"], value=description, inline=False)
                
                embed.set_footer(text=(f"Showing {results_to_display} "
                                       f"of {len(data)} results."))
                
                await ctx.send(embed=embed)
                logger.info("Data retrieved!")
            else:
                message = "Connection failed, or that isn't a word. :<"
                await ctx.send(message)
                logger.warning(message)

def setup(bot):
    """Setup function for Wikipedia."""
    bot.add_cog(Dictionary())
