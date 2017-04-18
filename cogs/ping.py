#!/usr/bin/env python3

# Standard modules
import datetime
import logging

# Third party modules
from discord.ext import commands

logger = logging.getLogger(__name__)

class Core:
    """discord.py cog containing a ping command."""
    
    @commands.command()
    async def ping(self, ctx):
        """Ping the bot."""
        pingtime = int(round((datetime.datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000, 0))
        await ctx.send(f":ping_pong: {pingtime} ms!")

def setup(bot):
    """Setup function for ping."""
    bot.add_cog(Core())
