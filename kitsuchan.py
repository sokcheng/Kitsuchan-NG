#!/usr/bin/env python3

"""A modular Discord bot, written in Python 3."""

# Standard modules
import sys
import datetime
import logging
import traceback

# Third-party modules
import asyncio
import discord
from discord.ext import commands

# Bundled modules
import app_info
import errors
import ext
import settings

assert (sys.version_info >= (3,6)), "This program requires Python 3.6 or higher."
assert (discord.version_info >= (1,0)), "This program requires Discord 1.0 or higher."

# Initialization
FORMAT = "%(asctime)-15s: %(message)s"
formatter = logging.Formatter(FORMAT)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
file_handler_logger = logging.FileHandler("discord.log")
file_handler_logger.setFormatter(formatter)
file_handler_logger.setLevel(logging.INFO)
logger.addHandler(file_handler_logger)

bot = ext.Bot(command_prefix=commands.when_mentioned, pm_help=True)
bot.description = app_info.DESCRIPTION

# Checking functions
@bot.check
def is_human(ctx):
    """Prevent the bot from responding to other bots."""
    return not ctx.author.bot

@bot.check
def is_public(ctx):
    """Prevent the bot from responding to DMs, unless it's the bot owner sending the DM."""
    if ctx.author.id == bot.owner_id:
        return True
    elif isinstance(ctx.channel, discord.DMChannel):
        raise commands.NoPrivateMessage("You are not allowed to DM this bot.")
    return True

# Events
@bot.listen("on_ready")
async def when_ready():
    """Conduct preparations once the bot is ready to go."""
    bot.time_started = datetime.datetime.now()
    
    # This hack forces bot.owner_id to be set internally by discord.py.
    await bot.is_owner(bot.user)
    
    username_spaceless = bot.user.name.lower().replace(" ", "")[:3]
    command_prefix_three_letters = f"{username_spaceless}"
    command_prefix_three_letters_space = f"{username_spaceless} "
    additional_prefixes = [command_prefix_three_letters_space, command_prefix_three_letters]
    
    command_prefix_custom = settings.manager.get("COMMAND_PREFIX")
    if isinstance(command_prefix_custom, str):
        additional_prefixes.append(command_prefix_custom)
    bot.command_prefix = commands.when_mentioned_or(*additional_prefixes)
    
    game = discord.Game()
    if isinstance(command_prefix_custom, str):
        game.name = f"{command_prefix_custom}help"
    else:
        game.name = f"{command_prefix_three_letters_space}help or @{bot.user.name} help"
    
    await bot.change_presence(game=game)
    logger.info(f"Bot is ONLINE! Username: {bot.user.name}, User ID: {bot.user.id}")

@bot.listen("on_command_completion")
async def help_sent(ctx):
    """Trigger when a command completes successfully."""
    if not isinstance(ctx.channel, discord.DMChannel):
        if ctx.command.name == "help":
            try:
                await ctx.send("Help sent to DM.")
            except discord.Forbidden:
                pass

@bot.listen("on_command_error")
async def handle_error(ctx, exception):
    """Handle errors that occur in commands."""
    
    # This section checks if the bot's owner DM'ed the bot the command.
    # The point of this is that the owner can debug the bot easily.
    is_owner = await bot.is_owner(ctx.author)
    if isinstance(ctx.channel, discord.DMChannel) and is_owner:
        await ctx.author.send(f"`{exception.__class__.__name__}`\n`{exception}`")
        return
    
    if isinstance(exception, commands.MissingRequiredArgument):
        await ctx.send(f"Please specify `{exception.param}` and try again. :<")
        logger.warning(exception)
    elif isinstance(exception, (commands.BadArgument, commands.UserInputError)) \
    or (isinstance(exception, commands.CommandInvokeError) \
        and isinstance(exception.original, (discord.HTTPException,
                                            ModuleNotFoundError))):
        try:
            await ctx.send(f"{exception} x.x")
        except discord.Forbidden:
            pass
        logger.warning(exception)
    elif isinstance(exception, commands.NoPrivateMessage):
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command in a DM."))
    elif isinstance(exception, commands.CommandOnCooldown):
        await ctx.send(("Command on cooldown; "
                        f"try again after {exception.retry_after:.2f} seconds. :<"))
        logger.warning(f"A command is being spammed too much by {ctx.author.name} ({ctx.author.id}).")
    elif isinstance(exception, errors.NSFWDisallowed):
        await ctx.send("Channel must be marked as NSFW to use that. x.x")
    elif isinstance(exception, commands.NotOwner):
        await ctx.send("Only the owner may do that. :<")
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command but "
                        f"was denied. Attempted command: {ctx.invoked_with}"))
    elif isinstance(exception, commands.CheckFailure):
        await ctx.send(("Permission denied. "
                        "Check your permissions and my permissions and try again. :<"))
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command but "
                        f"was denied. Attempted command: {ctx.invoked_with}"))
    else:
        logger.warning(f"{exception.__class__.__name__}:{exception}")
    exception = traceback.format_exc()
    logger.warning(exception)

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
    try:
        settings.manager["SUPPORT_GUILD"]
    except KeyError:
        print("Please enter a support guild link for this bot. You may leave it blank.")
        settings.manager["SUPPORT_GUILD"] = input("> ")
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
