#!/usr/bin/env python3

import logging

from discord.ext import commands

logger = logging.getLogger(__name__)

BASE_URL_STRAWPOLL = "https://strawpoll.me/{0}"
BASE_URL_STRAWPOLL_API = "https://strawpoll.me/api/v2/polls"

class StrawPoll:
    
    @commands.command()
    @commands.cooldown(100, 60)
    async def makepoll(self, ctx, title:str, *options):
        """Create a Straw Poll.
        
        Example usage:
        
        kit makepoll "Name of poll" "Option 1" "Option 2" Option3
        """
        if len(options) < 2:
            raise commands.UserInputError("Please specify at least two options!")
        logger.info("POSTing to Straw Poll API.")
        data = {"title": title, "options": options}
        async with ctx.bot.session.request("POST", BASE_URL_STRAWPOLL_API, json=data) as response:
            if response.status <= 210:
                logger.info("POSTing OK.")
                data = await response.json()
                url = BASE_URL_STRAWPOLL.format(data["id"])
                message = f"Successfully created poll; you can find it at {url}"
                await ctx.send(message)
            else:
                await ctx.send("Failed to create poll. x.x")
                logger.info("POSTing failed.")

def setup(bot):
    bot.add_cog(StrawPoll())
