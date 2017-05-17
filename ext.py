#!/usr/bin/env python3

import asyncio
import logging

import aiohttp
from discord.ext import commands

logger = logging.getLogger('discord')

class Bot(commands.Bot):
    """Custom bot object with additional helper functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # This bot has a global aiohttp.ClientSession to manage HTTP connections.
        self.session = aiohttp.ClientSession(loop=self.loop)
        
        # Add commands as an alias of help. Ignore this awful thing.
        self.all_commands["help"].aliases = ["commands"]
        self.all_commands["commands"] = self.all_commands["help"]
        
        # Store background tasks for management and possible eventual deletion.
        # Nested dictionary with syntax [module_name][task_name]
        self.background_tasks = {}
    
    """
    The following mechanisms allow us to add background tasks to the bot such that they can be
    deleted at any later point.
    """
    
    def add_task(self, module:str, coro):
        """Add a background task to the bot.
        
        * module - The name of the module that the task is found in. Use self.__module__ for this.
        * coro - The coroutine to be added as a background task.
        """
        self.background_tasks.setdefault(module, {})
        if not asyncio.iscoroutine(coro):
            logger.info(f"{coro.__name__} is not a coroutine!")
        else:
            self.background_tasks[module][coro.__name__] = self.loop.create_task(coro)
            logger.info(f"Registered background task {coro.__name__}!")
    
    def remove_task(self, module:str, name:str):
        """Remove a background task from the bot.
        
        Generally, you won't be calling this manually, as it's called within bot.unload_extension()
        
        * module - The name of the module that the task is found in.
        * coro - The name of the coroutine to be removed.
        """
        try:
            self.background_tasks[module][name].cancel()
            del self.background_tasks[module][name]
            logger.info(f"Unregistered background task {name}!")
        except KeyError:
            logger.info(f"{name} is not a registered background task!")
    
    def unload_extension(self, name:str):
        """Removes any background tasks associated with the extension."""
        
        # Remove background tasks.
        self.background_tasks.setdefault(name, {})
        for key_task in list(self.background_tasks[name].keys()):
            self.remove_task(name, key_task)
        if len(self.background_tasks[name]) == 0:
            del self.background_tasks[name]
        
        super().unload_extension(name)
    
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
