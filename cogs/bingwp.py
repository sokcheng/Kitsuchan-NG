#!/usr/bin/env python3

import random

from discord.ext import commands

BASE_URL_BING_API = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={0}&mkt=en-US"
BASE_URL_BING = "https://www.bing.com{0}"

systemrandom = random.SystemRandom()

class Wallpapers:

    @commands.command(aliases=["bwp"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def bingwp(self, ctx, wallpaper_count:int=None):
        """Query Bing for a wallpaper. Optional number of wallpapers.
        
        * wallpaper_count - The number of wallpapers requested."""
        
        url = BASE_URL_BING_API.format(wallpaper_count if wallpaper_count else 1000)

        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
            else:
                message = "Could not fetch URL."
                raise commands.UserInputError(message)

        if wallpaper_count:
            quote = []
            for index in range(0, min(len(data["images"]), wallpaper_count)):
                url = BASE_URL_BING.format(data["images"][index]["url"])
                quote.append(url)
            quote = "\n".join(quote)
        else:
            image = systemrandom.choice(data["images"])
            quote = BASE_URL_BING.format(image["url"])
        
        await ctx.send(quote)

def setup(bot):
    bot.add_cog(Wallpapers())
