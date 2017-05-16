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
GUNS = ("http://safebooru.org/samples/79/sample_d848db3fbe3fc8dc0f2cbb328f3af71c4e49989f.jpg",
        "http://safebooru.org/images/121/af2b15dbcd0a8feac03a4b990a600837724c84ec.jpg",
        "http://safebooru.org/images/1652/3f6d218b2433c9fe4e80f29a1a95eace88188f87.png",
        "http://safebooru.org/images/1591/ff08983843fe399487629927d2e10bc8a9dc51d2.jpg")

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
