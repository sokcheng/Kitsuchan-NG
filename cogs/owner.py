#!/usr/bin/env python3

# Standard modules
import logging
import subprocess

# Third party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Owner:
    """Commands that are only for the bot owner."""
    
    @commands.command()
    @commands.is_owner()
    async def rename(self, ctx, *, username):
        """Change the bot's username. Bot owner only."""
        await ctx.bot.user.edit(username=username)
        logger.info(f"Username changed to {username}.")
        await ctx.send(f"Username changed. :3")
    
    @commands.command(aliases=["listguilds"])
    @commands.is_owner()
    async def listg(self, ctx):
        """List all guilds that the bot is in. Bot owner only."""
        paginator = commands.Paginator()
        paginator.add_line("Guilds this bot is in:")
        for guild in ctx.bot.guilds:
            num_humans = len([member for member in guild.members if not member.bot])
            num_bots = len([member for member in guild.members if member.bot])
            paginator.add_line(f"{guild.id}: {num_humans} humans, {num_bots} bots | {guild.name}")
        for page in paginator.pages:
            await ctx.author.send(page)
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Sent to DM!")
    
    @commands.command(aliases=["clean"])
    @commands.is_owner()
    async def censor(self, ctx, times:int=1):
        """Delete the bot's previous message(s). Bot owner only.
        
        * times - Number of message to delete. Defaults to 1."""
        if times < 1:
            return commands.UserInputError("Can't delete less than 1 message.")
        times_executed = 0
        async for message in ctx.channel.history():
            if times_executed == times:
                break
            if message.author.id == ctx.bot.user.id:
                await message.delete()
                times_executed += 1
    
    @commands.command(aliases=["say"])
    @commands.is_owner()
    async def echo(self, ctx, *, text=""):
        """Repeat the user's text back at them. Bot owner only.
        
        * text - A string to be echoed back.
        """
        if len(text) == 0:
            text = "Echo?"
        # This mostly prevents the bot from triggering other bots.
        text = "\u200B" + text
        await ctx.send(text)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghelp(self, ctx):
        """Generate a file listing currently loaded commands. Bot owner only."""
        data = ["# List of commands",
                ("* Note 1: Some of these commands are in the [Kitsuchan-NG-cogs]"
                 "(https://github.com/n303p4/Kitsuchan-NG-cogs) repo."),
                "* Note 2: This file was automatically generated and may look bad."]
        for command in sorted(list(ctx.bot.commands), key=lambda x: x.name):
            data.append("")
            data.append(f"## {command.name}")
            if len(command.aliases) > 0:
                data.append("### Aliases: " + ", ".join(command.aliases))
            data.append(str(command.help))
        data = "\n".join(data)
        with open("COMMANDS.md", "w") as f:
            f.write(data)
        await ctx.send("Command list regenerated. :3")

def setup(bot):
    """Setup function for owner."""
    bot.add_cog(Owner())
