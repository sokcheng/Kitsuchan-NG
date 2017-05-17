#!/usr/bin/env python3

# Standard library
import asyncio
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import helpers
import settings
import utils

logger = logging.getLogger(__name__)

FILENAME_BLACKLIST = "blacklist.json"

class Blacklisting:
    """Blacklisting commands, to prevent abusive usage of the bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.bot.check(self.blacklist_user)
        self.bot.check(self.blacklist_guild)     
        self.bot.add_task(self.__module__, self.prune_guilds_auto())
        self.settings = {}
        self.load()
        
        @bot.listen("on_guild_join")
        async def check_guild(guild):
            reason = await self.prune_guild(guild)
            num_humans = helpers.count_humans(guild)
            num_bots = helpers.count_bots(guild)
            if not reason:
                logger.info(f"Joined guild {guild.name} ({guild.id})")
                for channel in self.bot.logging_channels:
                    await channel.send((f"Joined new guild **{guild.name}** ({guild.id})\n"
                                        f"**Owner:** {guild.owner.name} ({guild.owner.id})\n"
                                        f"**Humans:** {num_humans}\n"
                                        f"**Bots:** {num_bots}\n"
                                        f"**Region:** {guild.region}"))
            else:
                logger.info((f"Automatically left guild {guild.name} ({guild.id}) "
                             f"(reason: {reason})"))
                for channel in self.bot.logging_channels:
                    await channel.send((f"Rejected new guild **{guild.name}** ({guild.id}) "
                                        f"(reason: {reason})\n"
                                        f"**Owner:** {guild.owner.name} ({guild.owner.id})\n"
                                        f"**Humans:** {num_humans}\n"
                                        f"**Bots:** {num_bots}\n"
                                        f"**Region:** {guild.region}"))

        @bot.listen("on_guild_remove")
        async def guild_left_why(guild):
            for channel in self.bot.logging_channels:
                await channel.send(f"Got the boot from **{guild.name}** ({guild.id}).")

    async def prune_guild(self, guild:discord.Guild):
        """Automatically prune a guild."""
        num_humans = helpers.count_humans(guild)
        num_bots = helpers.count_bots(guild)
        collection = (num_bots/(num_bots + num_humans) >= 0.6) and num_bots > 20
        reason = None
        logger.debug(f"Checking guild {guild.name} ({guild.id}) (collection: {collection})...")
        if collection:
            await guild.leave()
            return "bot collection"
        elif guild.id in self.settings.get("GUILDS"):
            await guild.leave()
            return "guild blacklisted"
        elif guild.owner.id in self.settings.get("USERS"):
            await guild.leave()
            return "user blacklisted"

    async def prune_guilds(self):
        """Automatically leave guilds."""
        number = 0
        for guild in self.bot.guilds:
            reason = await self.prune_guild(guild)
            if reason:
                logger.info((f"Automatically left guild {guild.name} ({guild.id}) "
                             f"(reason: {reason})"))
                number += 1
        if number > 0:
            logger.info(f"{number} guilds were pruned.")
        return number

    async def prune_guilds_auto(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await self.prune_guilds()
            await asyncio.sleep(60)

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
        """Blocking commands (e.g. block user).
        
        Only the bot owner can use this."""
        embed = helpers.generate_help_embed(self.block)
        await ctx.send(embed=embed)

    @block.command(name="user")
    @commands.is_owner()
    async def _blockuser(self, ctx, user_id:int):
        """Block a user. Only the bot owner can use this.
        
        * user_id - The ID of the user to block.
        """
        self.settings.setdefault("USERS", [])
        app_info = await ctx.bot.application_info()
        is_owner = user_id == app_info.owner.id
        if is_owner:
            message = "Can't block bot owner."
            logger.warning(message)
            raise commands.UserInputError(message)
        if user_id not in self.settings["USERS"]:
            self.settings["USERS"].append(user_id)
            message = f"{user_id} blocked."
            logger.info(message)
            await ctx.send(message)
            await self.prune_guilds()
        else:
            message = f"{user_id} already blocked."
            logger.info(message)
            await ctx.send(message)
        self.save()

    @block.command(name="guild", aliases=["server"])
    @commands.is_owner()
    async def _blockguild(self, ctx, guild_id:int):
        """Block a guild. Only the bot owner can use this.
        
        * guild_id - The ID of the guild to block.
        """
        self.settings.setdefault("GUILDS", [])
        if guild_id not in self.settings["GUILDS"]:
            self.settings["GUILDS"].append(303302730213097473)
            message = f"{guild_id} blocked."
            logger.info(message)
            await ctx.send(message)
            try:
                guild = ctx.bot.get_guild(guild_id)
                await self.prune_guild(guild)
            except Exception:
                pass
        else:
            message = f"{guild.name} already blocked."
            logger.info(message)
            await ctx.send(message)
        self.save()

    @commands.group(aliases=["ublock"], invoke_without_command=True)
    @commands.is_owner()
    async def unblock(self, ctx):
        """Unblocking commands (e.g. unblock user).
        
        Only the bot owner can use this."""
        embed = helpers.generate_help_embed(self.unblock)
        await ctx.send(embed=embed)

    @unblock.command(name="user")
    @commands.is_owner()
    async def _unblockuser(self, ctx, user_id:int):
        """Unblock a user. Only the bot owner can use this.
        
        * user_id - The user ID to unblock.
        """
        self.settings.setdefault("USERS", [])
        if user_id in self.settings["USERS"]:
            self.settings["USERS"].remove(user_id)
            message = f"{user_id} unblocked."
            logger.info(message)
            await ctx.send(message)
        else:
            await ctx.send(f"{user_id} already unblocked.")
        self.save()

    @unblock.command(name="guild", aliases=["server"])
    @commands.is_owner()
    async def _unblockguild(self, ctx, guild_id:int):
        """Unblock a guild. Only the bot owner can use this.
        
        * guild_id - The ID of the guild to unblock.
        """
        self.settings.setdefault("GUILDS", [])
        if guild_id in self.settings["GUILDS"]:
            self.settings["GUILDS"].remove(guild_id)
            message = f"{guild_id} unblocked."
            logger.info(message)
            await ctx.send(message)
        else:
            message = f"{guild_id} already unblocked."
            logger.info(message)
            await ctx.send(message)
        self.save()

def setup(bot):
    bot.add_cog(Blacklisting(bot))
