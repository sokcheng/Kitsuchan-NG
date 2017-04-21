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
import errors
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
    if isinstance(ctx.channel, discord.DMChannel):
        raise commands.NoPrivateMessage("You are not allowed to DM this bot.")
    return True

# Events
@bot.event
async def on_ready():
    """Conduct preparations once the bot is ready to go."""
    bot.time_started = datetime.datetime.now()
    
    command_prefix_three_letters = f"{bot.user.name[:3].lower()}"
    command_prefix_three_letters_space = f"{bot.user.name[:3].lower()} "
    additional_prefixes = [command_prefix_three_letters_space, command_prefix_three_letters]
    
    command_prefix_custom = settings.manager.get("COMMAND_PREFIX")
    if isinstance(command_prefix_custom, str):
        additional_prefixes.append(command_prefix_custom)
    bot.command_prefix = commands.when_mentioned_or(*additional_prefixes)
    
    game = discord.Game()
    if isinstance(command_prefix_custom, str):
        game.name = f"{bot.command_prefix}help"
    else:
        game.name = f"{command_prefix_three_letters_space}help or @{bot.user.name} help"
    
    await bot.change_presence(game=game)
    logger.info(f"Bot is ONLINE! Username: {bot.user.name}, User ID: {bot.user.id}")

@bot.event
async def on_command_completion(ctx):
    """Trigger when a command completes successfully."""
    if not isinstance(ctx.channel, discord.DMChannel):
        if ctx.command.name == "help":
            await ctx.send("Help sent to DM.")

@bot.event
async def on_command_error(exception, ctx):
    """Handle errors that occur in commands."""
    
    # This section checks if the bot's owner DM'ed the bot the command.
    # The point of this is that the owner can debug the bot easily.
    is_owner = await bot.is_owner(ctx.author)
    if isinstance(ctx.channel, discord.DMChannel) and is_owner:
        await ctx.author.send(f"`{exception.__class__.__name__}`\n`{exception}`")
        return
    
    if isinstance(exception, (commands.BadArgument,
                              commands.MissingRequiredArgument,
                              commands.UserInputError)) \
    or (isinstance(exception, commands.CommandInvokeError) \
        and isinstance(exception.original, (discord.HTTPException,
                                            ModuleNotFoundError))):
        await ctx.send(f"{exception} x.x")
        logger.warning(exception)
    elif isinstance(exception, commands.NotOwner):
        await ctx.send("Only the owner can do that. :<")
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command but "
                        "was denied."))
    elif isinstance(exception, commands.NoPrivateMessage):
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command in a DM."))
    elif isinstance(exception, commands.CommandOnCooldown):
        await ctx.send(("Command on cooldown; "
                        f"try again after {exception.retry_after:.2f} seconds. :<"))
        logger.warning("A command is being spammed too much.")
    elif isinstance(exception, errors.NSFWDisallowed):
        await ctx.send("Channel must have `nsfw` in its name to use that. x.x")
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
