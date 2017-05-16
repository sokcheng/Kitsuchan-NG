#!/usr/bin/env python3

import resource

from discord.ext import commands

class Memchecker:

    def __init__(self, bot):
    
        self.previous_memory_usage = 0
        
        @bot.listen("on_command_completion")
        async def check_memory(ctx):
            memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if memory_usage != self.previous_memory_usage:
                for channel in bot.logging_channels:
                    await channel.send((f"Memory usage is now {memory_usage} KB "
                                        f"(following `{ctx.message.content}`)"))
                self.previous_memory_usage = memory_usage

        @bot.listen("on_guild_join")
        async def check_memory(ctx):
            memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if memory_usage != self.previous_memory_usage:
                for channel in bot.logging_channels:
                    await channel.send((f"Memory usage is now {memory_usage} KB "
                                        "(following guild join)"))
                self.previous_memory_usage = memory_usage

        @bot.listen("on_guild_remove")
        async def check_memory(ctx):
            memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if memory_usage != self.previous_memory_usage:
                for channel in bot.logging_channels:
                    await channel.send((f"Memory usage is now {memory_usage} KB "
                                        "(following guild leave)"))
                self.previous_memory_usage = memory_usage

def setup(bot):
    bot.add_cog(Memchecker(bot))
