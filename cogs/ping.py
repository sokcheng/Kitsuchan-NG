#!/usr/bin/env python3

# Standard modules
import datetime
import logging
import random

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
import helpers

systemrandom = random.SystemRandom()

logger = logging.getLogger(__name__)

VARIANTS = {"bang": ":gun: **BANG!**",
            "bang!": ":gun: **BANG!**",
            "beep": ":robot: Beep beep, I'm a bot!",
            "beep!": ":robot: Beep beep, I'm a bot!"}
GUNS = ("http://i.imgur.com/s6SMlIT.jpg",
        "http://i.imgur.com/GPZsqyr.jpg",
        "http://i.imgur.com/TQI7PZ0.png",
        "http://i.imgur.com/5hxnDDq.jpg")

class Ping:
    """Ping command."""
    
    @commands.command(aliases=list(VARIANTS.keys()) + ["pong"])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def ping(self, ctx):
        """Ping the bot."""
        pingtime = int(round((datetime.datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000, 0))
        if ctx.invoked_with in VARIANTS:
            variant = VARIANTS[ctx.invoked_with]
        else:
            variant = ":ping_pong:"
        message = f"{variant} {pingtime} ms!"
        embed = None
        if "bang" in ctx.invoked_with:
            if not helpers.has_scanning(ctx):
                embed = discord.Embed()
                embed.set_image(url=systemrandom.choice(GUNS))
            else:
                message = "\n".join((message, systemrandom.choice(GUNS)))
        await ctx.send(message, embed=embed)
        logger.info(f"Ping! False ping time: {pingtime} ms")

def setup(bot):
    """Setup function for ping."""
    bot.add_cog(Ping())
