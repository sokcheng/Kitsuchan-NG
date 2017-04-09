#!/usr/bin/env python3

"""Contains a cog for Rem resource API commands."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import utils

BASE_URL_API = "https://rra.ram.moe/i/r?type=%s"
BASE_URL_IMAGE = "https://rra.ram.moe/%s"

logger = logging.getLogger(__name__)

class Fun:
    """discord.py cog containing Rem resource API commands."""
    def __init__(self, bot):
        self.bot = bot

    async def get(self, ctx, kind:str, member:discord.Member=None):
        """A helper function that grabs an image and posts it in response to a member.
        
        kind - The type of image to retrieve.
        member - The member to mention in the command."""
        logger.info(f"Fetching {kind} image.")
        hash_id_channel = utils.to_hash(str(ctx.channel.id))
        url = BASE_URL_API % (kind)
        async with self.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                embed = discord.Embed(color=utils.random_color())
                url_image = BASE_URL_IMAGE % (data["path"],)
                embed.set_image(url=url_image)
                if not member:
                    message=None
                elif ctx.author.id != member.id:
                    message=f"**{member.mention}, you got a {kind} from {ctx.author.display_name}!**"
                else:
                    message=f"**{member.mention}, I'm so sorry. Have a {kind} anyway.**"
                await ctx.send(message, embed=embed)
            else:
                message = "Could not retrieve image. :("
                await ctx.send(message)
                logger.info(message)

    @commands.command()
    async def cry(self, ctx):
        """Cry!"""
        await self.get(ctx, "cry")

    @commands.command()
    async def cuddle(self, ctx, member:discord.Member):
        """Cuddle a member!
        
        member - The member to be cuddled."""
        await self.get(ctx, "cuddle", member)

    @commands.command()
    async def hug(self, ctx, member:discord.Member):
        """Hug a member!
        
        member - The member to be hugged."""
        await self.get(ctx, "hug", member)
        
    @commands.command()
    async def kiss(self, ctx, member:discord.Member):
        """Kiss a member!
        
        member - The member to be kissed."""
        await self.get(ctx, "kiss", member)

    @commands.command()
    async def lewd(self, ctx):
        """Lewd!"""
        await self.get(ctx, "lewd")

    @commands.command()
    async def lick(self, ctx, member:discord.Member):
        """Lick a member!
        
        member - The member to be licked."""
        await self.get(ctx, "lick", member)

    @commands.command()
    async def nom(self, ctx):
        """Nom!"""
        await self.get(ctx, "nom")

    @commands.command()
    async def nyan(self, ctx):
        """Nyan!"""
        await self.get(ctx, "nyan")

    @commands.command()
    async def pout(self, ctx):
        """Pout!"""
        await self.get(ctx, "pout")

    @commands.command()
    async def slap(self, ctx, member:discord.Member):
        """Slap a member!
        
        member - The member to be slapped."""
        await self.get(ctx, "slap")

    @commands.command()
    async def smug(self, ctx):
        """Smug!"""
        await self.get(ctx, "smug")

    @commands.command()
    async def stare(self, ctx, member:discord.Member):
        """Stare at a member!
        
        member - The member to be stared at."""
        await self.get(ctx, "stare", member)

    @commands.command()
    async def tickle(self, ctx, member:discord.Member):
        """Tickle a member!
        
        member - The member to be tickled."""
        await self.get(ctx, "tickle", member)

    @commands.command()
    async def triggered(self, ctx):
        """Triggered!"""
        await self.get(ctx, "triggered")

def setup(bot):
    """Setup function for Reactions."""
    bot.add_cog(Fun(bot))
