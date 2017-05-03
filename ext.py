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

    # Redefine all the event coros so that we have our own event handling system.
    # There REALLY has to be a better way of doing it than this. But for now, it will do. :|
    
    # Basic group
    async def on_ready(self):
        coros = self.event_coroutines.get("on_ready", {})
        for coro in coros.values():
            try:
                await coro()
            except Exception:
                continue
    
    async def on_error(self, *args, **kwargs):
        coros = self.event_coroutines.get("on_error", {})
        for coro in coros.values():
            try:
                await coro(*args, **kwargs)
            except Exception:
                continue
    
    # Message group
    async def on_message(self, message):
        super().on_message(message)
        coros = self.event_coroutines.get("on_message", {})
        for coro in coros.values():
            try:
                await coro(message)
            except Exception:
                continue
    
    async def on_message_delete(self, message):
        coros = self.event_coroutines.get("on_message_delete", {})
        for coro in coros.values():
            try:
                await coro(message)
            except Exception:
                continue
    
    async def on_message_edit(self, message):
        coros = self.event_coroutines.get("on_message_edit", {})
        for coro in coros.values():
            try:
                await coro(message)
            except Exception:
                continue
    
    # Reaction group
    async def on_reaction_add(self, reaction, user):
        coros = self.event_coroutines.get("on_reaction_add", {})
        for coro in coros.values():
            try:
                await coro(reaction, user)
            except Exception:
                continue
    
    async def on_reaction_remove(self, reaction, user):
        coros = self.event_coroutines.get("on_reaction_remove", {})
        for coro in coros.values():
            try:
                await coro(reaction, user)
            except Exception:
                continue
    
    async def on_reaction_clear(self, message, reactions):
        coros = self.event_coroutines.get("on_reaction_clear", {})
        for coro in coros.values():
            try:
                await coro(message, reactions)
            except Exception:
                continue
    
    # Channel group
    async def on_channel_delete(self, channel):
        coros = self.event_coroutines.get("on_channel_delete", {})
        for coro in coros.values():
            try:
                await coro(channel)
            except Exception:
                continue
    
    async def on_channel_create(self, channel):
        coros = self.event_coroutines.get("on_channel_create", {})
        for coro in coros.values():
            try:
                await coro(channel)
            except Exception:
                continue
    
    async def on_channel_update(self, before, after):
        coros = self.event_coroutines.get("on_channel_update", {})
        for coro in coros.values():
            try:
                await coro(before, after)
            except Exception:
                continue
    
    # Member group
    async def on_member_join(self, member):
        coros = self.event_coroutines.get("on_member_join", {})
        for coro in coros.values():
            try:
                await coro(member)
            except Exception:
                continue
    
    async def on_member_remove(self, member):
        coros = self.event_coroutines.get("on_member_remove", {})
        for coro in coros.values():
            try:
                await coro(member)
            except Exception:
                continue
    
    async def on_member_update(self, before, after):
        coros = self.event_coroutines.get("on_member_update", {})
        for coro in coros.values():
            try:
                await coro(before, after)
            except Exception:
                continue
    
    # Guild group
    async def on_guild_join(self, guild):
        coros = self.event_coroutines.get("on_guild_join", {})
        for coro in coros.values():
            try:
                await coro(guild)
            except Exception:
                continue

    async def on_guild_remove(self, guild):
        coros = self.event_coroutines.get("on_guild_remove", {})
        for coro in coros.values():
            try:
                await coro(guild)
            except Exception:
                continue
    
    async def on_guild_update(self, before, after):
        coros = self.event_coroutines.get("on_guild_update", {})
        for coro in coros.values():
            try:
                await coro(before, after)
            except Exception:
                continue
    
    # Command group
    async def on_command(self, ctx):
        coros = self.event_coroutines.get("on_command", {})
        for coro in coros.values():
            try:
                await coro(ctx)
            except Exception:
                continue
    
    async def on_command_error(self, exc, ctx):
        super().on_message(*args, **kwargs)
        coros = self.event_coroutines.get("on_command_error", {})
        for coro in coros.values():
            try:
                await coro(exc, ctx)
            except Exception:
                continue
    
    async def on_command_completion(self, ctx):
        coros = self.event_coroutines.get("on_command_completion", {})
        for coro in coros.values():
            try:
                await coro(ctx)
            except Exception:
                continue

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
