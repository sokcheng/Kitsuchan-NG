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
BASE_URL_DUCKDUCKGO = "https://duckduckgo.com/?{0}"

async def _duckduckgo(ctx, *, query):
    """Retrieve an answer from DuckDuckGo, using the Instant Answers JSON API.
    
    * query - A list of strings to be used in the search criteria.
    
    This command is both powerful and dangerous! It isn't its own command for a reason.
    """
    if len(query) == 0:
        message = "Query not specified."
        raise commands.UserInputError("", message)
    logger.info(f"Retrieving DuckDuckGo answer with tags {query}.")
    params = urllib.parse.urlencode({"q": query, "t": "ffsb",
                                     "format": "json", "ia": "answer"})
    url = BASE_URL_DUCKDUCKGO.format(params)
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
    async def anagram(self, ctx, *, phrase:str):
        """Find possible anagrams of a phrase.
        
        * phrase = The message to find an anagram for."""
        query = f"find anagram for {phrase}"
        answer = await _duckduckgo(ctx, query=query)
        if answer:
            await ctx.send(answer)
        else:
            await ctx.send("No anagrams found. :<")

class Crypto:

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def atbash(self, ctx, *, phrase:str):
        """Convert text using a reversed alphabet.
        
        * phrase = The message to be encoded."""
        query = f"atbash {phrase}"
        answer = await _duckduckgo(ctx, query=query)
        answer = answer.replace("Atbash: ", "", 1)
        await ctx.send(answer)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def base64(self, ctx, *, phrase:str):
        """Convert a phrase into Base64.
        
        * phrase = The text to convert."""
        query = f"base64 {phrase}"
        answer = await _duckduckgo(ctx, query=query)
        answer = answer.replace("Base64 encode d: ", "")
        await ctx.send(answer)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def rot13(self, ctx, *, phrase:str):
        """Convert a phrase into ROT13.
        
        * phrase = The text to convert."""
        query = f"rot13 {phrase}"
        answer = await _duckduckgo(ctx, query=query)
        answer = answer.replace("ROT13: ", "", 1)
        await ctx.send(answer)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def sha3(self, ctx, *, phrase:str):
        """Convert a phrase into its SHA-3 hash.
        
        * phrase = The text to convert."""
        query = f"sha3 {phrase}"
        answer = await _duckduckgo(ctx, query=query)
        await ctx.send(answer)

def setup(bot):
    """Setup function for DuckDuckGo."""
    bot.add_cog(Fortune())
    bot.add_cog(Words())
    bot.add_cog(Crypto())
