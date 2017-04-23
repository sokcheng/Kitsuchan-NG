#!/usr/bin/env python3

# Standard modules
import logging

# Third-party libraries
import discord
from discord.ext import commands

# Bundled modules
import helpers

logger = logging.getLogger(__name__)

class Encoding:
    """Commands that encode and decode text."""
    
    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def reverse(self, ctx, *, message):
        """Reverse input text."""
        logger.info("Reversing text.")
        await ctx.send(message[::-1])
    
    @commands.group(invoke_without_command=True)
    async def to(self, ctx):
        """Subcommands that encode plaintext. (e.g. to binary)"""
        embed = helpers.generate_help_embed(self.to)
        await ctx.send(embed=embed)
    
    @to.command(name="binary")
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def to_binary(self, ctx, *, message):
        """Encode plaintext to binary.
        
        Note, the behavior of this command isn't 100% correct as it may slip on Unicode."""
        logger.info("Converting a message to binary.")
        message = list(message)
        for index in range(len(message)):
            message[index] = str(bin(ord(message[index])))[2:].zfill(8)
        message = " ".join(message)
        await ctx.send(message)
    
    @commands.group(name="from", invoke_without_command=True)
    async def from_(self, ctx):
        """Subcommands that decode plaintext. (e.g. from binary)"""
        embed = helpers.generate_help_embed(self.from_)
        await ctx.send(embed=embed)
    
    @from_.command(name="binary")
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def from_binary(self, ctx, *, message):
        """Decode plaintext from binary.
        
        Note, the behavior of this command isn't 100% correct as it may slip on Unicode."""
        logger.info("Converting a message from binary.")
        message = message.split()
        for index in range(len(message)):
            try:
                message[index] = chr(int(f"0b{message[index]}", base=2))
            except ValueError:
                pass
        message = "".join(message)
        await ctx.send(message)
    
def setup(bot):
    bot.add_cog(Encoding())
