#!/usr/bin/env python3

"""This cog contains DuckDuckGo query commands."""

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

logger = logging.getLogger(__name__)

# Constants
BASE_URL_DUCKDUCKGO = "https://duckduckgo.com/?%s"

async def _duckduckgo(ctx, *, query):
    """Retrieve an answer from DuckDuckGo, using the Instant Answers JSON API.
    
    * query - A list of strings to be used in the search criteria.
    
    This command is both powerful and dangerous! It isn't its own command for a reason.
    """
    if len(query) == 0:
        message = "Query not specified."
        raise commands.UserInputError("", message)
    logger.info("Retrieving DuckDuckGo answer with tags %s." % (query,))
    params = urllib.parse.urlencode({"q": query, "t": "ffsb",
                                     "format": "json", "ia": "answer"})
    url = BASE_URL_DUCKDUCKGO % params
    async with ctx.bot.session.get(url) as response:
        if response.status == 200:
            # This should be response.json() directly, but DuckDuckGo returns an incorrect MIME.
            data = await response.text()
            data = json.loads(data)
            if len(data) == 0:
                raise errors.ZeroDataLengthError()
            answer = html.unescape(data["Answer"])
            logger.info("Answer retrieved!")
            return answer
        else:
            message = "Failed to fetch answer. :("
            logger.info(message)
            return message

class Temperature:

    @commands.command(name="f2c")
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def fahrenheit_to_celsius(self, ctx, temperature:int):
        """Convert temperature in Fahrenheit to Celsius.
        
        * temperature - An integer representing temperature in Fahrenheit."""
        query = f"{temperature} f in c"
        answer = await _duckduckgo(ctx, query=query)
        await ctx.send(answer)

    @commands.command(name="c2f")
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def celsius_to_fahrenheit(self, ctx, temperature:int):
        """Convert temperature in Celsius to Fahrenheit.
        
        * temperature - An integer representing temperature in Celsius."""
        query = f"{temperature} c in f"
        answer = await _duckduckgo(ctx, query=query)
        await ctx.send(answer)

class Fortune:

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def fortune(self, ctx):
        """Produce a random fortune. :3"""
        answer = await _duckduckgo(ctx, query="random fortune")
        await ctx.send(answer)

class Words:

    @commands.command(aliases=["randomname"])
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def rname(self, ctx):
        """Generate a random name."""
        answer = await _duckduckgo(ctx, query="random name")
        answer = answer.replace("(random)", "")
        await ctx.send(answer)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def anagram(self, ctx, *, text:str):
        """Find possible anagrams of a phrase.
        
        * text = The message to find an anagram for."""
        query = f"find anagram for {text}"
        answer = await _duckduckgo(ctx, query=query)
        if answer:
            await ctx.send(answer)
        else:
            await ctx.send("No anagrams found. :<")

class Crypto:

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def atbash(self, ctx, *, text:str):
        """Convert text using a reversed alphabet.
        
        * text = The message to be encoded."""
        query = f"atbash {text}"
        answer = await _duckduckgo(ctx, query=query)
        answer = answer.replace("Atbash: ", "", 1)
        await ctx.send(answer)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def base64(self, ctx, *, text:str):
        """Convert a phrase into Base64.
        
        * text = The text to convert."""
        query = f"base64 {text}"
        answer = await _duckduckgo(ctx, query=query)
        answer = answer.replace("Base64 encode d: ", "")
        await ctx.send(answer)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def rot13(self, ctx, *, text:str):
        """Convert a phrase into ROT13.
        
        * text = The text to convert."""
        query = f"rot13 {text}"
        answer = await _duckduckgo(ctx, query=query)
        answer = answer.replace("ROT13: ", "", 1)
        await ctx.send(answer)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def sha3(self, ctx, *, text:str):
        """Convert a phrase into its SHA-3 hash.
        
        * text = The text to convert."""
        query = f"sha3 {text}"
        answer = await _duckduckgo(ctx, query=query)
        await ctx.send(answer)

def setup(bot):
    """Setup function for DuckDuckGo."""
    bot.add_cog(Temperature())
    bot.add_cog(Fortune())
    bot.add_cog(Words())
    bot.add_cog(Crypto())
    bot.add_cog(Web())