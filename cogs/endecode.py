#!/usr/bin/env python3

# Third-party libraries
import discord
from discord.ext import commands

# Bundled modules
import helpers

class Utilities:
    """A cog containing commands that encode/decode text in some form or another."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def reverse(self, ctx, *, message):
        """Reverse input text."""
        await ctx.send(message[::-1])
    
    @commands.group(invoke_without_command=True)
    async def to(self, ctx):
        """Subcommands that encode plaintext. (e.g. to binary)"""
        embed = await helpers.generate_help_embed(self._to)
        await ctx.send(embed=embed)
    
    @to.command(name="binary")
    async def to_binary(self, ctx, *, message):
        """Encode plaintext to binary.
        
        Note, the behavior of this command isn't 100% correct as it may slip on Unicode."""
        message = list(message)
        for index in range(len(message)):
            message[index] = str(bin(ord(message[index])))[2:].zfill(8)
        message = " ".join(message)
        await ctx.send(message)
    
    @commands.group(name="from", invoke_without_command=True)
    async def from_(self, ctx):
        """Subcommands that decode plaintext. (e.g. from binary)"""
        embed = await helpers.generate_help_embed(self._from)
        await ctx.send(embed=embed)
    
    @from_.command(name="binary")
    async def from_binary(self, ctx, *, message):
        """Decode binary to plaintext.
        
        Note, the behavior of this command isn't 100% correct as it may slip on Unicode."""
        message = message.split()
        for index in range(len(message)):
            try:
                message[index] = chr(int(f"0b{message[index]}", base=2))
            except ValueError:
                pass
        message = "".join(message)
        await ctx.send(message)
    
def setup(bot):
    bot.add_cog(Utilities(bot))
