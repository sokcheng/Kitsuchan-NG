#!/usr/bin/env python3

"""Contains a cog with the bot's core commands."""

# Standard modules
import sys
import os
import datetime
import logging
import subprocess

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
from __main__ import __file__ as FILE_MAIN # This sucks
import app_info
import helpers
import settings
import utils

logger = logging.getLogger(__name__)

class Core:
    """discord.py cog containing core functions of the bot.
    
    bot - The parent discord.Client object for the cog.
    logger - A logger to assign the cog.
    """
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        """Display information about this bot, such as library versions."""
        logger.info("Displaying info about the bot.")
        uptime = str(datetime.datetime.now() - self.bot.time_started).split(".")[0]
        embed = discord.Embed()
        embed.description = self.bot.description
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        ainfo = await self.bot.application_info()
        owner = ainfo.owner.mention
        embed.add_field(name="Version", value=app_info.VERSION_STRING)
        embed.add_field(name="Owner", value=owner)
        num_guilds = len(self.bot.guilds)
        num_users = len([0 for member in self.bot.get_all_members()])
        embed.add_field(name="Serving", value=f"{num_users} users in {num_guilds} guilds")
        embed.add_field(name="Uptime", value=uptime)
        embed.add_field(name="Python", value="{0}.{1}.{2}".format(*sys.version_info))
        embed.add_field(name="discord.py", value=discord.__version__)
        try:
            cookies_eaten = sum(discord.version_info[:3]) * sum(app_info.VERSION[:3])
            embed.add_field(name="Cookies eaten", value=str(cookies_eaten))
        except Exception:
            pass
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["listguilds"])
    @commands.is_owner()
    async def listg(self, ctx):
        paginator = commands.Paginator()
        for guild in self.bot.guilds:
            paginator.add_line(f"{guild.name} ({guild.id})")
        for page in paginator.pages:
            await ctx.author.send(page)
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Sent to DM!")
    
    @commands.command()
    @commands.is_owner()
    async def censor(self, ctx, times:int=1):
        """Delete the bot's previous message(s).
        
        * times - Number of message to delete. Defaults to 1."""
        if times < 1:
            return commands.UserInputError("Can't delete less than 1 message.")
        logger.info(f"Deleting {times} previous messages.")
        times_executed = 0
        async for message in ctx.channel.history():
            if times_executed == times:
                break
            if message.author.id == self.bot.user.id:
                await message.delete()
                times_executed += 1
    
    @commands.command(aliases=["say"])
    @commands.is_owner()
    async def echo(self, ctx, *text):
        """Repeat the user's text back at them.
        
        * *text - A list of strings, which is concatenated into one string before being echoed.
        """
        message = " ".join(text)
        logger.info(f"ctx.author.display_name {ctx.author.id} requested echo of {message}")
        if len(message) == 0:
            message = "Echo?"
        # Split the message up by zero-width spaces so the bot doesn't trigger other bots.
        message = "\u200B"*8 + message
        await ctx.send(message)
    
    @commands.command()
    @commands.is_owner()
    async def halt(self, ctx):
        """Halt the bot. Must be bot owner to execute."""
        confirm = await helpers.yes_no(ctx, self.bot)
        if not confirm:
            return
        message = "Bot is going for halt NOW!"
        logger.warning(message)
        await ctx.send(message)
        await self.bot.logout()
        settings.save()
        self.bot.session.close()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot. Must be bot owner to execute."""
        confirm = await helpers.yes_no(ctx, self.bot)
        if not confirm:
            return
        message = "Bot is going for restart NOW!"
        logger.warning(message)
        await ctx.send(message)
        await self.bot.logout()
        self.bot.session.close()
        settings.save()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    @commands.command(aliases=["load-extension"])
    @commands.is_owner()
    async def loade(self, ctx, extension_name:str):
        """Enable the use of an extension."""
        logger.info(f"Loading extension {extension_name}...")
        self.bot.load_extension(extension_name)
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        if extension_name not in settings.manager["EXTENSIONS"]:
            settings.manager["EXTENSIONS"].append(extension_name)
            message = f"Extension {extension_name} loaded."
        else:
            message = f"Extension {extension_name} is already loaded. :<"
        await ctx.send(message)
        logger.info(message)

    @commands.command(aliases=["reload-extension"])
    @commands.is_owner()
    async def rloade(self, ctx, extension_name:str):
        """Reload an already-loaded extension."""
        logger.info(f"Reloading extension {extension_name}...")
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        if extension_name in settings.manager["EXTENSIONS"]:
            self.bot.unload_extension(extension_name)
            self.bot.load_extension(extension_name)
            message = f"Extension {extension_name} reloaded."
        else:
            message = f"Extension {extension_name} not currently loaded; please load it. :<"
        await ctx.send(message)
        logger.info(message)

    @commands.command(aliases=["unload-extension"])
    @commands.is_owner()
    async def uloade(self, ctx, extension_name:str):
        """Disable the use of an extension."""
        prompt = await helpers.yes_no(ctx, self.bot)
        if not prompt:
            return
        logger.info(f"Unloading extension {extension_name}...")
        self.bot.unload_extension(extension_name)
        settings.manager.setdefault("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
        try:
            settings.manager["EXTENSIONS"].remove(extension_name)
        except ValueError:
            message = f"Extension {extension_name} is already unloaded. :<"
        else:
            message = f"Extension {extension_name} unloaded."
        await ctx.send(message)
        logger.info(message)

    @commands.command(aliases=["list-extensions"])
    @commands.is_owner()
    async def liste(self, ctx):
        """Display list of currently-enabled bot extensions."""
        logger.info("Extension list requested.")
        extensions = "\n".join(self.bot.extensions)
        message = f"```Loaded extensions:\n{extensions}```"
        await ctx.author.send(message)
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Sent to DM!")

    @commands.command()
    @commands.is_owner()
    async def sh(self, ctx, *expression):
        """Execute a system command. Only the owner may run this."""
        if len(expression) == 0:
            raise commands.UserInputError("No command was specified.")
        logger.info(f"Shell execution of {expression} requested.")
        process = subprocess.Popen(expression,
                                   universal_newlines=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        try:
            output, errors = process.communicate(timeout=8)
            output = output[:1018]
            process.terminate()
        except subprocess.TimeoutExpired:
            process.kill()
            output = "Command timed out. x.x"
        embed = discord.Embed()
        string_expression = " ".join(expression)
        embed.add_field(name="Input", value=f"```{string_expression}```", inline=False)
        embed.add_field(name="Output", value=f"```{output}```", inline=False)
        await ctx.send(embed=embed)
        logger.info(f"Execution of {expression} complete. Output:\n{output}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ghelp(self, ctx):
        """Generate a file listing commands that the bot is capable of."""
        data = ["# List of commands",
                ("* Note 1: Some of these commands are in the [Kitsuchan-NG-cogs]"
                 "(https://github.com/n303p4/Kitsuchan-NG-cogs) repo."),
                "* Note 2: This file was automatically generated and may look bad."]
        for command in sorted(list(self.bot.commands), key=lambda x: x.name):
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
    """Setup function for Core."""
    bot.add_cog(Core(bot))
