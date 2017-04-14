#!/usr/bin/env python3

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import settings
import helpers

FILENAME_BLACKLIST = "blacklist.json"

class Core:
    """This cog contains blacklisting functions."""
    def __init__(self, bot):
        self.bot = bot
        self.bot.check(self.blacklist_guild)
        self.settings = {}
        self.load()
    
    def load(self):
        try:
            self.settings = settings.load(FILENAME_BLACKLIST)
        except Exception:
            self.save()
    
    def save(self):
        self.settings.setdefault("GUILDS", [])
        settings.save(FILENAME_BLACKLIST, self.settings)
    
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
    
    @user.command()
    @commands.is_owner()
    async def block(self, ctx, user:discord.User):
        """Unblock a user.
        
        * user - The user to block.
        """
        if not user.is_blocked():
            await user.block()
            await ctx.send(f"{user.name} ({user.id}) blocked.")
        else:
            await ctx.send(f"{user.name} is already blocked.")
    
    @user.command()
    @commands.is_owner()
    async def unblock(self, ctx, user:discord.User):
        """Unblock a user.
        
        * user - The user to unblock.
        """
        if user.is_blocked():
            await user.unblock()
            await ctx.send(f"{user.name} ({user.id}) unblocked.")
        else:
            await ctx.send(f"{user.name} is already unblocked.")
    
    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def guild(self, ctx):
        """Guild blocking and unblocking commands."""
        embed = helpers.generate_help_embed(self.guild)
        await ctx.send(embed=embed)
    
    @guild.command()
    @commands.is_owner()
    async def block(self, ctx, id_guild:int=None):
        """Block a guild.
        
        * id_guild - The ID of the guild to block. Defaults to current guild.
        """
        if not id_guild and ctx.guild:
            guild = ctx.guild
        else:
            guild = self.bot.get_guild(id_guild)
        if not guild:
            raise commands.UserInputError(f"Guild ID {id_guild} isn't valid.")
        self.settings.setdefault("GUILDS", [])
        if guild.id not in self.settings["GUILDS"]:
            self.settings["GUILDS"].append(guild.id)
            await ctx.send(f"{guild.name} blocked.")
            await guild.leave()
        else:
            await ctx.send(f"{guild.name} already blocked.")
        self.save()
    
    @guild.command()
    @commands.is_owner()
    async def unblock(self, ctx, id_guild:int):
        """Unblock a guild.
        
        * id_guild - The ID of the guild to unblock.
        """
        self.settings.setdefault("GUILDS", [])
        if id_guild in self.settings["GUILDS"]:
            self.settings["GUILDS"].remove(id_guild)
            await ctx.send(f"{id_guild} unblocked.")
        else:
            await ctx.send(f"{id_guild} already unblocked.")
        self.save()

def setup(bot):
    bot.add_cog(Core(bot))
