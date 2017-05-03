#!/usr/bin/env python3

import asyncio
import logging

from discord.ext import commands

FORMAT = "%(asctime)-15s: %(message)s"
formatter = logging.Formatter(FORMAT)

logger = logging.getLogger('commands.log')
logger.setLevel(logging.INFO)
file_handler_command_log = logging.FileHandler("commands.log")
file_handler_command_log.setFormatter(formatter)
file_handler_command_log.setLevel(logging.INFO)
logger.addHandler(file_handler_command_log)

class CommandLog:

    """The purpose of this cog is to log commands. Nothing more or less."""

    def __init__(self, bot):
        self.command_cache = []

        self.bot = bot

        @bot.add_to_event("on_command")
        async def log_command(ctx):
            message = f"Execution of {ctx.message.content} requested by {ctx.author.name} ({ctx.author.id})."
            logger.info(message)
            message = f"{ctx.message.created_at.ctime()}: {message}"
            
            # Append the command to the command_cache for further processing in the bot's logging behavior.
            self.command_cache.append(message)

        self.bot.loop.create_task(self.send_to_log_channel())

    # Background tasks
    async def send_to_log_channel(self):
        """This function logs commands and stuff."""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            if len(self.command_cache) > 0:
                paginator = commands.Paginator()
                for index in range(0, len(self.command_cache)):
                    paginator.add_line(self.command_cache[0])
                    del self.command_cache[0]
                for channel in self.bot.logging_channels:
                    for page in paginator.pages:
                        await channel.send(page)
            await asyncio.sleep(1800)

def setup(bot):
    bot.add_cog(CommandLog(bot))
