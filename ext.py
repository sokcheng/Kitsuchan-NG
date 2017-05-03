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
        
        # This stores a huge mass of coroutines for events.
        self.event_coroutines = {}
        
        # Dynamically create event handlers.
        for name in ("on_ready", "on_error",
                     "on_message_delete", "on_message_edit",
                     "on_reaction_add", "on_reaction_remove", "on_reaction_clear",
                     "on_channel_delete", "on_channel_create", "on_channel_update",
                     "on_member_join", "on_member_remove", "on_member_update",
                     "on_guild_join", "on_guild_remove", "on_guild_update",
                     "on_guild_role_create", "on_guild_role_delete", "on_guild_role_update",
                     "on_guild_emojis_update",
                     "on_guild_available", "on_guild_unavailable",
                     "on_member_ban", "on_member_unban",
                     "on_typing",
                     "on_command", "on_command_completion", "on_command_error"):
            event = self.create_event_handler(name)
            setattr(self, name, event)

    def create_event_handler(self, name:str):
        """This function dynamically creates a generic event handler."""
        async def event_handler(*args, **kwargs):
            coros = self.event_coroutines.get(name, {})
            for coro in coros.values():
                try:
                    await coro(*args, **kwargs)
                except Exception:
                    continue
        return event_handler

    """
    The following mechanisms allow us to add coroutines to an event, in contrast to d.py's
    @bot.event decorator which only allows us to specify one at a time.
    """
    
    def add_to_event(self, event:str):
        """This is a decorator that adds a coroutine to an event on the bot.
        
        Example usage:
        
        @bot.add_to_event("on_ready")
        async def handle_readiness():
            pass
        """
        def decorator(coro):
            if not asyncio.iscoroutinefunction(coro):
                logger.info(f"{coro.__name__} is not a valid coroutine!")
            else:
                self.event_coroutines.setdefault(event, {})
                self.event_coroutines[event][coro.__name__] = coro
                logger.info(f"Successfully added coroutine {coro.__name__} to event {event}!")
        return decorator

    def remove_from_event(self, event:str, name:str):
        """Remove a coroutine from an event on the bot. This is not a decorator.
        
        * event - The type of event we want to remove the coroutine from.
        * name - The name of the coroutine we want to get rid of.
        
        Example usage:
        
        bot.remove_from_event("on_ready", "handle_readiness")
        """
        self.event_coroutines.setdefault(event, {})
        del self.event_coroutines[event][name]
        logger.info(f"Successfully removed coroutine {name} from event {event}!")

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
