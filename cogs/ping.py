#!/usr/bin/env python3

# Standard modules
import datetime
import logging

# Third party modules
from discord.ext import commands

logger = logging.getLogger(__name__)

VARIANTS = {"bang": ":gun: **BANG!**",
            "bang!": ":gun: **BANG!**"}

class Ping:
    """Ping command."""
    
    @commands.command(aliases=["bang", "bang!", "pong"])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def ping(self, ctx):
        """Ping the bot."""
        pingtime = int(round((datetime.datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000, 0))
        if ctx.invoked_with in VARIANTS:
            variant = VARIANTS[ctx.invoked_with]
        else:
            variant = ":ping_pong:"
        await ctx.send(f"{variant} {pingtime} ms!")
        logger.info(f"Ping! False ping time: {pingtime} ms")

def setup(bot):
    """Setup function for ping."""
    bot.add_cog(Ping())
