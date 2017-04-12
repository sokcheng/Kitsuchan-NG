#!/usr/bin/env python3

"""Contains a cog for various weeb reaction commands."""

# Standard modules
import logging
import random

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import helpers
import utils

logger = logging.getLogger(__name__)

# Base URL strings for RRA API.
BASE_URL_API = "https://rra.ram.moe/i/r?type=%s"
BASE_URL_IMAGE = "https://rra.ram.moe/%s"

# Single image links.
IMAGE_DEAD = "https://s-media-cache-ak0.pinimg.com/736x/ec/61/ef/ec61ef110a5d2e01bf8ae48331b63723.jpg"
IMAGE_FACEDESK = "https://media.tumblr.com/tumblr_lqegp8wjxZ1qktqch.gif"
IMAGE_LMLY = "https://68.media.tumblr.com/tumblr_mej070O7Lj1qktqch.gif"
IMAGE_WHAT = "https://media.tumblr.com/tumblr_lnvtzjiY4J1qktqch.png"
IMAGE_WLOL = "https://68.media.tumblr.com/tumblr_lqehb0eOK01qktqch.jpg"

# Tuples of image links.
IMAGES_BOOTS = (("https://media-cache-ak0.pinimg.com/736x/db/b9/a3/"
                 "dbb9a30cc312682ee2d2cc4cf84310ae.jpg"),
                 "https://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=21163978",
                 "https://i.imgur.com/3Y4r38i.jpg",
                 "https://i.imgur.com/Jj0eZTh.png",
                 "https://i.imgur.com/EC4UXCI.jpg")
IMAGES_LEWD = ("https://i.imgur.com/5JZH78a.jpg",
               "https://i.imgur.com/RdQ3FFA.jpg",
               "https://i.imgur.com/98tad3K.gif",
               "https://i.imgur.com/8Dd399u.gif",
               "https://i.imgur.com/NbZ5Wgo.png",
               "https://i.imgur.com/aFHmenc.gif",
               "https://i.imgur.com/OsckzUL.png",
               "https://i.imgur.com/3EZyiLQ.jpg",
               "https://i.imgur.com/AaZvqcF.jpg",
               "https://i.imgur.com/XzQRDDl.jpg",
               "https://i.imgur.com/GTfWFm6.jpg",
               "https://i.imgur.com/Iz315vJ.jpg",
               "https://i.imgur.com/rWLoIzf.png")
IMAGES_SANDWICHES = ("https://i.imgur.com/kyTDwIX.png",
                     "https://i.imgur.com/ULKlVhU.png",
                     "https://i.imgur.com/Z2RvlBx.png",
                     "https://i.imgur.com/k5GnTbU.png",
                     "https://i.imgur.com/SzuegH9.png",
                     "https://i.imgur.com/ppcHtKd.png",
                     "https://i.imgur.com/xy8iwN5.png")

class Reactions:
    """Cog containing various weeb reaction commands."""
    def __init__(self, bot):
        self.bot = bot

    async def _get(self, ctx, kind:str, member:discord.Member=None):
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
                elif self.bot.user.id == member.id:
                    message=f"**Aw, thank you. Here, have one back. :3**"
                elif ctx.author.id != member.id:
                    message=f"**{member.display_name}, you got a {kind} from {ctx.author.display_name}!**"
                else:
                    message=f"**{member.display_name}, I'm so sorry. Have a {kind} anyway.**"
                await ctx.send(message, embed=embed)
            else:
                message = "Could not retrieve image. :("
                await ctx.send(message)
                logger.info(message)

    async def _send_image(self, ctx, url_image):
        """A helper function that creates an embed with an image and sends it off."""
        embed = discord.Embed(color=utils.random_color())
        if isinstance(url_image, tuple):
            embed.set_image(url=random.choice(url_image))
        elif isinstance(url_image, str):
            embed.set_image(url=url_image)
        else:
            embed.description = str(url_image)
        await ctx.send(embed=embed)

    @commands.command()
    async def dead(self, ctx):
        """Dead!"""
        await self._send_image(ctx, IMAGE_DEAD)

    @commands.command(aliases=["facedesk"])
    async def fdesk(self, ctx):
        """Facedesk!"""
        await self._send_image(ctx, IMAGE_FACEDESK)

    @commands.command(aliases=["letmeloveyou"])
    async def lmly(self, ctx):
        """Let me love you!"""
        await self._send_image(ctx, IMAGE_LMLY)

    @commands.command()
    async def what(self, ctx):
        """What?"""
        await self._send_image(ctx, IMAGE_WHAT)

    @commands.command(aliases=["wakarimasenlol"])
    async def wlol(self, ctx):
        """Wakarimasen, lol!"""
        await self._send_image(ctx, IMAGE_WLOL)

    @commands.command()
    async def boots(self, ctx):
        """Boots!"""
        await self._send_image(ctx, IMAGES_BOOTS)

    @commands.command()
    async def sandwich(self, ctx):
        """Sandwich!"""
        await self._send_image(ctx, IMAGES_SANDWICHES)

    @commands.command()
    async def cry(self, ctx):
        """Cry!"""
        await self._get(ctx, "cry")

    @commands.command()
    async def cuddle(self, ctx, member:discord.Member):
        """Cuddle a member!
        
        * member - The member to be cuddled."""
        await self._get(ctx, "cuddle", member)

    @commands.command()
    async def hug(self, ctx, member:discord.Member):
        """Hug a member!
        
        * member - The member to be hugged."""
        await self._get(ctx, "hug", member)
        
    @commands.command()
    async def kiss(self, ctx, member:discord.Member):
        """Kiss a member!
        
        * member - The member to be kissed."""
        await self._get(ctx, "kiss", member)

    @commands.command()
    async def lewd(self, ctx):
        """Lewd!"""
        choice = bool(random.getrandbits(1))
        if choice:
            await self._get(ctx, "lewd")
        else:
            await ctx._send_image(ctx, IMAGES_LEWD)

    @commands.command()
    async def lick(self, ctx, member:discord.Member):
        """Lick a member!
        
        * member - The member to be licked."""
        await self._get(ctx, "lick", member)

    @commands.command()
    async def nom(self, ctx):
        """Nom!"""
        await self._get(ctx, "nom")

    @commands.command()
    async def nyan(self, ctx):
        """Nyan!"""
        await self._get(ctx, "nyan")

    @commands.command()
    async def owo(self, ctx):
        """owo"""
        await self._get(ctx, "owo")

    @commands.command()
    async def pat(self, ctx, member:discord.Member):
        """Pat a member!
        
        * member - The member to be patted."""
        await self._get(ctx, "pat", member)

    @commands.command()
    async def pout(self, ctx):
        """Pout!"""
        await self._get(ctx, "pout")

    @commands.command()
    async def slap(self, ctx, member:discord.Member):
        """Slap a member!
        
        * member - The member to be slapped."""
        await self._get(ctx, "slap", member)

    @commands.command()
    async def smug(self, ctx):
        """Smug!"""
        await self._get(ctx, "smug")

    @commands.command()
    async def stare(self, ctx, member:discord.Member):
        """Stare at a member!
        
        member - The member to be stared at."""
        await self._get(ctx, "stare", member)

    @commands.command()
    async def tickle(self, ctx, member:discord.Member):
        """Tickle a member!
        
        member - The member to be tickled."""
        await self._get(ctx, "tickle", member)

    @commands.command()
    async def triggered(self, ctx):
        """Triggered!"""
        await self._get(ctx, "triggered")

def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Reactions(bot))
