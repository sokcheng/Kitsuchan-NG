#!/usr/bin/env python3

"""A modular Discord bot, written in Python 3."""

# Standard modules
import sys
import datetime
import logging

# Third-party modules
import aiohttp
import discord
from discord.ext import commands

# Bundled modules
import app_info
import settings

assert (sys.version_info >= (3,6)), "This program requires Python 3.6 or higher."
assert (discord.version_info >= (1,0)), "This program requires Discord 1.0 or higher."

# Initialization
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = commands.Bot(command_prefix=commands.when_mentioned, pm_help=True)
bot.description = app_info.DESCRIPTION
bot.session = aiohttp.ClientSession(loop=bot.loop)

# Checking functions
@bot.check
def is_human(ctx):
    """Prevent the bot from responding to other bots."""
    return not ctx.author.bot

@bot.check
def is_public(ctx):
    """Prevent the bot from responding to DMs, unless it's the bot owner sending the DM."""
    if bot.is_owner(ctx.author):
        return True
    return not isinstance(ctx.channel, discord.DMChannel)

# Events
@bot.event
async def on_ready():
    """Conduct preparations once the bot is ready to go."""
    bot.time_started = datetime.datetime.now()
    command_prefix = settings.manager.get("COMMAND_PREFIX")
    if isinstance(command_prefix, str):
        bot.command_prefix = command_prefix
    game = discord.Game()
    if callable(bot.command_prefix):
        game.name = f"@{bot.user.name} help"
    else:
        game.name = f"{bot.command_prefix}help"
    await bot.change_presence(game=game)
    logger.info(f"Bot is ONLINE! Username: {bot.user.name}, User ID: {bot.user.id}")

@bot.event
async def on_command_completion(ctx):
    """Trigger when a command completes successfully."""
    if not isinstance(ctx.channel, discord.DMChannel):
        if ctx.invoked_with == "help":
            await ctx.send("Help sent to DM.")

@bot.event
async def on_command_error(exception, ctx):
    """Handle errors that occur in commands."""
    
    # This section checks if the bot's owner DM'ed the bot the command.
    # The point of this is that the owner can debug the bot easily.
    if isinstance(ctx.channel, discord.DMChannel) and bot.is_owner(ctx.author):
        await ctx.author.send(f"`{exception.__class__.__name__}`\n`{exception}`")
        return
    
    if isinstance(exception, (commands.BadArgument,
                              commands.MissingRequiredArgument,
                              commands.UserInputError)) \
    or (isinstance(exception, commands.CommandInvokeError) \
        and isinstance(exception.original, (discord.HTTPException,
                                            ModuleNotFoundError))):
        embed = discord.Embed(title="Error! x.x", color=discord.Color.red())
        embed.description = str(exception)
        await ctx.send(embed=embed)
        logger.warning(exception)
    elif isinstance(exception, commands.NotOwner):
        await ctx.send("Only the owner can do that. :<")
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command but "
                        "was denied."))
    elif isinstance(exception, commands.NoPrivateMessage):
        await ctx.send("Can't do that outside of a guild. :<")
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command but "
                        "was denied."))
    elif isinstance(exception, commands.CommandOnCooldown):
        await ctx.send(("Command on cooldown; "
                        f"try again after {exception.retry_after:.2f} seconds. :<"))
        logger.warning("A command is being spammed too much.")
    elif isinstance(exception, commands.CheckFailure):
        await ctx.send("No. Now move your hands away from that command. :<")
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command but "
                        "was denied."))
    else:
        logger.warning(f"{exception.__class__.__name__}:{exception}")

def main():
    """It's the main function. You call this to start the bot."""
    try:
        settings.load()
    except (FileNotFoundError or IOError or json.decoder.JSONDecodeError):
        settings.save()
    try:
        settings.manager["OAUTH_TOKEN_DISCORD"]
    except KeyError:
        print("Please enter an OAuth token for this bot, so it can sign into Discord.")
        settings.manager["OAUTH_TOKEN_DISCORD"] = input("> ")
    logger.info("Warming up...")
    extensions = settings.manager.get("EXTENSIONS", settings.DEFAULT_EXTENSIONS)
    
    for extension in extensions:
        logger.info(f"Loading extension {extension}")
        try:
            bot.load_extension(extension)
            logger.info(f"Extension {extension} loaded")
        except Exception as error:
            logger.warning(f"Extension {extension} seems to be broken")
            logger.warning(error)
    
    bot.run(settings.manager["OAUTH_TOKEN_DISCORD"])

if __name__ == "__main__":
    main()
