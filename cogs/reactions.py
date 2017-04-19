#!/usr/bin/env python3

"""Contains a cog for various weeb reaction commands."""

# Standard modules
import logging
import random

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import checks
import utils

logger = logging.getLogger(__name__)

systemrandom = random.SystemRandom()

# Base URL strings for RRA API.
BASE_URL_API = "https://rra.ram.moe/i/r?type={0}"
BASE_URL_IMAGE = "https://wia.ram.moe{0[path]}"

# Single image links.
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
IMAGES_DEAD = (("https://s-media-cache-ak0.pinimg.com/736x/ec/61/ef/"
                "ec61ef110a5d2e01bf8ae48331b63723.jpg"),
               "http://safebooru.org//images/2048/60ce6f6888ba2fce6393638223dcc8d7c67f0655.jpg")
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
IMAGES_POKE = ("http://safebooru.org//images/1880/e3b020472d86b0a04ffec8cdf41049ef66cf3a68.gif",
               "http://safebooru.org//images/2051/031566980728255e6d7e2fba8c12a3c38ea7598a.gif",
               "http://safebooru.org//images/1169/3edae332d38c887a8723207d1bc0dffac8244591.gif")
IMAGES_SANDWICHES = ("https://i.imgur.com/kyTDwIX.png",
                     "https://i.imgur.com/ULKlVhU.png",
                     "https://i.imgur.com/Z2RvlBx.png",
                     "https://i.imgur.com/k5GnTbU.png",
                     "https://i.imgur.com/SzuegH9.png",
                     "https://i.imgur.com/ppcHtKd.png",
                     "https://i.imgur.com/xy8iwN5.png")
IMAGES_KONKON = ("http://safebooru.org//images/1856/6e6b3319f2a0a3fe5e77567ebdc998b3c4cb3900.jpg",
                 "http://safebooru.org//samples/1832/sample_25adf8a37226fa003a6a6d7b0f3171f5764bba7d.jpg",
                 "http://safebooru.org//images/1270/a9c1744fb4676f743c4dbc7668a39e72decdde16.jpg",
                 "http://safebooru.org//images/2077/12bddb7bd2274f0ba9abe2d72c994555d562e0df.jpg")

class Reactions:
    """Cog containing various weeb reaction commands."""

    async def _rra(self, ctx, kind:str, member:discord.Member=None):
        """A helper function that grabs an image and posts it in response to a member.
        
        * kind - The type of image to retrieve.
        * member - The member to mention in the command."""
        logger.info(f"Fetching {kind} image.")
        hash_id_channel = utils.to_hash(str(ctx.channel.id))
        url = BASE_URL_API.format(kind)
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                url_image = BASE_URL_IMAGE.format(data).replace("/i", "")
                if not member:
                    message=""
                elif ctx.bot.user.id == member.id:
                    message=f"Aw, thank you. Here, have one back. :3"
                elif ctx.author.id != member.id:
                    message=f"**{member.display_name}**, you got a {kind} from **{ctx.author.display_name}!**"
                else:
                    message=f"**{member.display_name}**, I'm so sorry. Have a {kind} anyway."
                if ctx.guild and ctx.guild.explicit_content_filter.name == "disabled":
                    embed = discord.Embed(color=utils.random_color())
                    embed.set_image(url=url_image)
                    await ctx.send(message, embed=embed)
                else:
                    message = "\n".join([str(message), url_image])
                    await ctx.send(message)
            else:
                message = "Could not retrieve image. :("
                await ctx.send(message)
                logger.info(message)

    async def _send_image(self, ctx, url_image):
        """A helper function that creates an embed with an image and sends it off."""
        if isinstance(url_image, (tuple, list)):
            url_image = systemrandom.choice(url_image)
        if ctx.guild and ctx.guild.explicit_content_filter.name == "disabled":
            embed = discord.Embed(color=utils.random_color())
            embed.set_image(url=url_image)
            await ctx.send(embed=embed)
        else:
            await ctx.send(url_image)

    # Commands based on _send_image()
    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def dead(self, ctx):
        """Dead!"""
        await self._send_image(ctx, IMAGES_DEAD)

    @commands.command(aliases=["facedesk"])
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def fdesk(self, ctx):
        """Facedesk!"""
        await self._send_image(ctx, IMAGE_FACEDESK)

    @commands.command(aliases=["konkon"])
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def kon(self, ctx):
        """Kon, kon!"""
        await self._send_image(ctx, IMAGES_KONKON)

    @commands.command(aliases=["letmeloveyou"])
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def lmly(self, ctx):
        """Let me love you!"""
        await self._send_image(ctx, IMAGE_LMLY)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def poke(self, ctx):
        """Poke!"""
        await self._send_image(ctx, IMAGES_POKE)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def what(self, ctx):
        """What?"""
        await self._send_image(ctx, IMAGE_WHAT)

    @commands.command(aliases=["wakarimasenlol"])
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def wlol(self, ctx):
        """Wakarimasen, lol!"""
        await self._send_image(ctx, IMAGE_WLOL)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def boots(self, ctx):
        """Boots!"""
        await self._send_image(ctx, IMAGES_BOOTS)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def sandwich(self, ctx):
        """Sandwich!"""
        await self._send_image(ctx, IMAGES_SANDWICHES)

    # Commands based on _rra()
    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def cry(self, ctx):
        """Cry!"""
        await self._rra(ctx, "cry")

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def cuddle(self, ctx, member:discord.Member):
        """Cuddle a member!
        
        * member - The member to be cuddled."""
        await self._rra(ctx, "cuddle", member)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def hug(self, ctx, member:discord.Member):
        """Hug a member!
        
        * member - The member to be hugged."""
        await self._rra(ctx, "hug", member)
        
    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def kiss(self, ctx, member:discord.Member):
        """Kiss a member!
        
        * member - The member to be kissed."""
        await self._rra(ctx, "kiss", member)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def lewd(self, ctx):
        """Lewd!"""
        choice = bool(random.getrandbits(1))
        if choice:
            await self._rra(ctx, "lewd")
        else:
            await self._send_image(ctx, IMAGES_LEWD)

    @commands.command()
    @commands.check(checks.is_nsfw)
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def lick(self, ctx, member:discord.Member):
        """Lick a member!
        
        * member - The member to be licked."""
        await self._rra(ctx, "lick", member)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def nom(self, ctx):
        """Nom!"""
        await self._rra(ctx, "nom")

    @commands.command(aliases=['nya', 'meow'])
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def nyan(self, ctx):
        """Nyan!"""
        await self._rra(ctx, "nyan")

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def owo(self, ctx):
        """owo"""
        await self._rra(ctx, "owo")

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def pat(self, ctx, member:discord.Member):
        """Pat a member!
        
        * member - The member to be patted."""
        await self._rra(ctx, "pat", member)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def pout(self, ctx):
        """Pout!"""
        await self._rra(ctx, "pout")

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def slap(self, ctx, member:discord.Member):
        """Slap a member!
        
        * member - The member to be slapped."""
        await self._rra(ctx, "slap", member)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def smug(self, ctx):
        """Smug!"""
        await self._rra(ctx, "smug")

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def stare(self, ctx, member:discord.Member):
        """Stare at a member!
        
        * member - The member to be stared at."""
        await self._rra(ctx, "stare", member)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def tickle(self, ctx, member:discord.Member):
        """Tickle a member!
        
        * member - The member to be tickled."""
        await self._rra(ctx, "tickle", member)

    @commands.command()
    @commands.cooldown(4, 12, commands.BucketType.channel)
    async def triggered(self, ctx):
        """Triggered!"""
        await self._rra(ctx, "triggered")

def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Reactions())
