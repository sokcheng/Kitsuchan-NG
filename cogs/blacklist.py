#!/usr/bin/env python3

# Standard library
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import settings
import helpers

logger = logging.getLogger('discord')

FILENAME_BLACKLIST = "blacklist.json"

class Core:
    """This cog contains blacklisting functions."""
    def __init__(self, bot):
        self.bot = bot
        self.bot.check(self.blacklist_user)
        self.bot.check(self.blacklist_guild)        
        self.settings = {}
        self.load()
        
        @self.bot.event
        async def on_guild_join(guild):
            if guild.id in self.settings.get("GUILDS"):
                await guild.leave()
    
    def load(self):
        try:
            self.settings = settings.load(FILENAME_BLACKLIST)
        except Exception:
            self.save()
    
    def save(self):
        self.settings.setdefault("USERS", [])
        self.settings.setdefault("GUILDS", [])
        settings.save(FILENAME_BLACKLIST, self.settings)
    
    def blacklist_user(self, ctx):
        if self.bot.is_owner(ctx.author):
            return True
        return ctx.author.id not in self.settings.get("USERS")
    
    def blacklist_guild(self, ctx):
        if ctx.guild:
            return ctx.guild.id not in self.settings.get("GUILDS")
        return True
    
    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def user(self, ctx):
        """User blocking and unblocking commands."""
        embed = helpers.generate_help_embed(self.user)
        await ctx.send(embed=embed)
    
    @user.command(name="block")
    @commands.is_owner()
    async def _blockuser(self, ctx, user:discord.User):
        """Block a user.
        
        * user - The user to block.
        """
        self.settings.setdefault("USERS", [])
        if self.bot.is_owner(user):
            message = "Can't block bot owner."
            logger.warning(message)
            raise commands.UserInputError(message)
        if user.id not in self.settings["USERS"]:
            self.settings["USERS"].append(user.id)
            message = f"{user.name} ({user.id}) blocked."
            logger.info(message)
            await ctx.send(message)
        else:
            message = f"{user.name} ({user.id}) already blocked."
            logger.info(message)
            await ctx.send(message)
        self.save()
    
    @user.command(name="unblock")
    @commands.is_owner()
    async def _unblockuser(self, ctx, user:discord.User):
        """Unblock a user.
        
        * user - The user to unblock.
        """
        self.settings.setdefault("USERS", [])
        if user.id in self.settings["USERS"]:
            self.settings["USERS"].remove(user.id)
            message = f"{user.name} ({user.id}) unblocked."
            logger.info(message)
            await ctx.send(message)
        else:
            await ctx.send(f"{user.name} ({user.id}) already unblocked.")
        self.save()
    
    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def guild(self, ctx):
        """Guild blocking and unblocking commands."""
        embed = helpers.generate_help_embed(self.guild)
        await ctx.send(embed=embed)
    
    @guild.command(name="block")
    @commands.is_owner()
    async def _blockguild(self, ctx, id_guild:int=None):
        """Block a guild.
        
        * id_guild - The ID of the guild to block. Defaults to current guild.
        """
        if not id_guild and ctx.guild:
            guild = ctx.guild
        else:
            guild = self.bot.get_guild(id_guild)
        if not guild:
            message = f"Guild ID {id_guild} isn't valid."
            logger.warning(message)
            raise commands.UserInputError(message)
        self.settings.setdefault("GUILDS", [])
        if guild.id not in self.settings["GUILDS"]:
            self.settings["GUILDS"].append(guild.id)
            message = f"{guild.name} blocked."
            logger.info(message)
            await ctx.send(message)
            await guild.leave()
        else:
            message = f"{guild.name} already blocked."
            logger.info(message)
            await ctx.send(message)
        self.save()
    
    @guild.command(name="unblock")
    @commands.is_owner()
    async def _unblockguild(self, ctx, id_guild:int):
        """Unblock a guild.
        
        * id_guild - The ID of the guild to unblock.
        """
        self.settings.setdefault("GUILDS", [])
        if id_guild in self.settings["GUILDS"]:
            self.settings["GUILDS"].remove(id_guild)
            message = f"{id_guild} unblocked."
            logger.info(message)
            await ctx.send(message)
        else:
            message = f"{id_guild} already unblocked."
            logger.info(message)
            await ctx.send(message)
        self.save()

def setup(bot):
    bot.add_cog(Core(bot))
