#!/usr/bin/env python3

# Standard library
import asyncio
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import settings
import helpers

logger = logging.getLogger(__name__)

FILENAME_BLACKLIST = "blacklist.json"

class Core:
    """This cog contains blacklisting functions."""
    def __init__(self, bot):
        self.bot = bot
        self.bot.check(self.blacklist_user)
        self.bot.check(self.blacklist_guild)     
        self.bot.loop.create_task(self.prune_guilds_auto())
        self.settings = {}
        self.load()
        
        @self.bot.event
        async def on_guild_join(guild):
            reason = await self.prune_guild(guild)
            app_info = await self.bot.application_info()
            if not reason:
                num_humans, num_bots = self.humans_vs_bots(guild)
                await app_info.owner.send((f"Joined new guild **{guild.name}** ({guild.id})\n"
                                           f"**Owner:** {guild.owner.name}\n"
                                           f"**Humans:** {num_humans}\n"
                                           f"**Bots:** {num_bots}\n"
                                           f"**Region:** {guild.region}"))
            else:
                await app_info.owner.send((f"Rejected joining **{guild.name}** ({guild.id}) "
                                           f"(reason: {reason})"))

    def humans_vs_bots(self, guild):
        num_humans = len([member for member in guild.members if not member.bot])
        num_bots = len([member for member in guild.members if member.bot])
        return num_humans, num_bots

    async def prune_guild(self, guild:discord.Guild):
        num_humans, num_bots = self.humans_vs_bots(guild)
        if guild.id in self.settings.get("GUILDS"):
            await guild.leave()
            logger.info(f"Automatically left guild {guild.name} ({guild.id})")
            return "blacklisted"
        elif num_bots > num_humans and num_bots > 6:
            await guild.leave()
            logger.info(f"Automatically left guild {guild.name} ({guild.id})")
            return "bot collection"

    async def prune_guilds(self):
        """Automatically leave guilds if they're found to be too bot-heavy."""
        logger.info("Pruning guilds.")
        number = 0
        for guild in self.bot.guilds:
            status = await self.prune_guild(guild)
            if status:
                number += 1
        logger.info(f"{number} guilds were pruned.")
        return number

    async def prune_guilds_auto(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.prune_guilds()
            await asyncio.sleep(30)

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
        return ctx.author.id not in self.settings.get("USERS")

    def blacklist_guild(self, ctx):
        if ctx.guild:
            return ctx.guild.id not in self.settings.get("GUILDS")
        return True

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def block(self, ctx):
        """Blocking commands (e.g. block user)."""
        embed = await helpers.generate_help_embed(self.block)
        await ctx.send(embed=embed)

    @block.command(name="user")
    @commands.is_owner()
    async def _blockuser(self, ctx, user:discord.User):
        """Block a user.
        
        * user - The user to block.
        """
        self.settings.setdefault("USERS", [])
        is_owner = await self.bot.is_owner(user)
        if is_owner:
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

    @block.command(name="guild", aliases=["server"])
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

    @commands.group(aliases=["ublock"], invoke_without_command=True)
    @commands.is_owner()
    async def unblock(self, ctx):
        """Unblocking commands. (e.g. unblock user)"""
        embed = await helpers.generate_help_embed(self.unblock)
        await ctx.send(embed=embed)

    @unblock.command(name="user")
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

    @unblock.command(name="guild", aliases=["server"])
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
