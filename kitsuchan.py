#!/usr/bin/env python3

"""A modular Discord bot, written in Python 3."""

# Standard modules
import sys
import datetime
import logging

# Third-party modules
import asyncio
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

command_log = logging.getLogger('command.log')
command_log.setLevel(logging.INFO)
file_handler_command_log = logging.FileHandler("commands.log")
file_handler_command_log.setLevel(logging.DEBUG)
command_log.addHandler(file_handler_command_log)

command_cache = []

bot = commands.Bot(command_prefix=commands.when_mentioned, pm_help=True)
bot.description = app_info.DESCRIPTION
bot._owner_id = None
bot.session = aiohttp.ClientSession(loop=bot.loop)

# Checking functions
@bot.check
def is_human(ctx):
    """Prevent the bot from responding to other bots."""
    return not ctx.author.bot

@bot.check
def is_public(ctx):
    """Prevent the bot from responding to DMs, unless it's the bot owner sending the DM."""
    if ctx.author.id == bot._owner_id:
        return True
    elif isinstance(ctx.channel, discord.DMChannel):
        raise commands.NoPrivateMessage("You are not allowed to DM this bot.")
    return True

# Events
@bot.event
async def on_command(ctx):
    message = f"Execution of {ctx.message.content} requested by {ctx.author.name} ({ctx.author.id})."
    command_log.info(message)
    message = f"{ctx.message.created_at.ctime()}: {message}"
    command_cache.append(message)

@bot.event
async def on_ready():
    """Conduct preparations once the bot is ready to go."""
    bot.time_started = datetime.datetime.now()
    
    app_info = await bot.application_info()
    bot._owner = app_info.owner
    bot._owner_id = app_info.owner.id
    
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
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command but "
                        f"was denied. Attempted command: {ctx.invoked_with}"))
    elif isinstance(exception, commands.NoPrivateMessage):
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command in a DM."))
    elif isinstance(exception, commands.CommandOnCooldown):
        await ctx.send(("Command on cooldown; "
                        f"try again after {exception.retry_after:.2f} seconds. :<"))
        logger.warning(f"A command is being spammed too much by {ctx.author.name} ({ctx.author.id}).")
    elif isinstance(exception, errors.NSFWDisallowed):
        await ctx.send("Channel must have `nsfw` in its name to use that. x.x")
    elif isinstance(exception, commands.CheckFailure):
        await ctx.send("No. Now move your hands away from that command. :<")
        logger.warning((f"{ctx.author.name} ({ctx.author.id}) tried to issue a command but "
                        f"was denied. Attempted command: {ctx.invoked_with}"))
    else:
        logger.warning(f"{exception.__class__.__name__}:{exception}")

# Background tasks
async def send_owner_commands():
    await bot.wait_until_ready()
    while not bot.is_closed():
        if len(command_cache) > 0 and hasattr(bot, "_owner"):
            paginator = commands.Paginator()
            for line in command_cache:
                paginator.add_line(command_cache.pop(0))
            for page in paginator.pages:
                await bot._owner.send(page)
        await asyncio.sleep(1800)

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
    
    bot.loop.create_task(send_owner_commands())
    bot.run(settings.manager["OAUTH_TOKEN_DISCORD"])

if __name__ == "__main__":
    main()
