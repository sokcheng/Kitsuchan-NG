#!/usr/bin/env python3

import aiohttp
from discord.ext import commands

class Bot(commands.Bot):
    """Custom bot object with additional helper functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # This bot has a global aiohttp.ClientSession to manage HTTP connections.
        self.session = aiohttp.ClientSession(loop=self.loop)
        
        # Add commands as an alias of help. Ignore this awful thing.
        self.all_commands["help"].aliases = ["commands"]
        self.all_commands["commands"] = self.all_commands["help"]

    async def logout(self):
        """The logout function must end the ClientSession as well."""
        await super().logout()
        self.session.close()

    @property
    def logging_channels(self):
        """Return a list of channels that the bot can use for logging purposes.
        
        Note that this requires the bot's owner_id attribute to be set!
        """
        channels = []
        
        for guild in self.guilds:
            if guild.owner.id == self.owner_id:
                for channel in guild.text_channels:
                    if channel.name == "log" or channel.name.startswith("log-"):
                        channels.append(channel)
        
        return channels
