#!/usr/bin/env python3

"""Contains a cog for Rem resource API commands."""

# Standard modules
import logging

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import helpers
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
        
        * kind - The type of image to retrieve.
        * member - The member to mention in the command."""
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
                    message=f"**{member.display_name}, you got a {kind} from {ctx.author.display_name}!**"
                else:
                    message=f"**{member.display_name}, I'm so sorry. Have a {kind} anyway.**"
                await ctx.send(message, embed=embed)
            else:
                message = "Could not retrieve image. :("
                await ctx.send(message)
                logger.info(message)

    @commands.group(aliases=["w"], invoke_without_command=True)
    async def rem(self, ctx):
        """Various weeb image subcommands."""
        embed = await helpers.generate_help_embed(self.rem)
        await ctx.send(embed=embed)

    @rem.command()
    async def cry(self, ctx):
        """Cry!"""
        await self.get(ctx, "cry")

    @rem.command()
    async def cuddle(self, ctx, member:discord.Member):
        """Cuddle a member!
        
        * member - The member to be cuddled."""
        await self.get(ctx, "cuddle", member)

    @rem.command()
    async def hug(self, ctx, member:discord.Member):
        """Hug a member!
        
        * member - The member to be hugged."""
        await self.get(ctx, "hug", member)
        
    @rem.command()
    async def kiss(self, ctx, member:discord.Member):
        """Kiss a member!
        
        * member - The member to be kissed."""
        await self.get(ctx, "kiss", member)

    @rem.command()
    async def lewd(self, ctx):
        """Lewd!"""
        await self.get(ctx, "lewd")

    @rem.command()
    async def lick(self, ctx, member:discord.Member):
        """Lick a member!
        
        * member - The member to be licked."""
        await self.get(ctx, "lick", member)

    @rem.command()
    async def nom(self, ctx):
        """Nom!"""
        await self.get(ctx, "nom")

    @rem.command()
    async def nyan(self, ctx):
        """Nyan!"""
        await self.get(ctx, "nyan")

    @rem.command()
    async def owo(self, ctx):
        """owo"""
        await self.get(ctx, "owo")

    @rem.command()
    async def pat(self, ctx, member:discord.Member):
        """Pat a member!
        
        * member - The member to be patted."""
        await self.get(ctx, "pat", member)

    @rem.command()
    async def pout(self, ctx):
        """Pout!"""
        await self.get(ctx, "pout")

    @rem.command()
    async def slap(self, ctx, member:discord.Member):
        """Slap a member!
        
        * member - The member to be slapped."""
        await self.get(ctx, "slap", member)

    @rem.command()
    async def smug(self, ctx):
        """Smug!"""
        await self.get(ctx, "smug")

    @rem.command()
    async def stare(self, ctx, member:discord.Member):
        """Stare at a member!
        
        member - The member to be stared at."""
        await self.get(ctx, "stare", member)

    @rem.command()
    async def tickle(self, ctx, member:discord.Member):
        """Tickle a member!
        
        member - The member to be tickled."""
        await self.get(ctx, "tickle", member)

    @rem.command()
    async def triggered(self, ctx):
        """Triggered!"""
        await self.get(ctx, "triggered")

def setup(bot):
    """Setup function for RRA."""
    bot.add_cog(Fun(bot))
