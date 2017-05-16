#!/usr/bin/env python3

"""This cog contains welcome messages. You probably shouldn't use this."""

# Standard modules
import logging

# Third-party modules
from discord.ext import commands

logger = logging.getLogger(__name__)

class Welcome:
    """Welcome messages."""

    def __init__(self, bot):
    
        @bot.listen("on_member_join")
        async def welcome(member):
            guild = member.guild
            await guild.default_channel.send((f"Welcome to **{guild.name}**, {member.mention}. "
                                              "Hope you enjoy your stay! :D"))

def setup(bot):
    """Setup function for Wikipedia."""
    bot.add_cog(Welcome(bot))
