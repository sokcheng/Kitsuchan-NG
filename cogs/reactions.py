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
import helpers
import utils

logger = logging.getLogger(__name__)

systemrandom = random.SystemRandom()

# Base URL strings for RRA API.
BASE_URL_API = "https://rra.ram.moe/i/r?type={0}"
BASE_URL_IMAGE = "https://wia.ram.moe{0[path]}"

# Single image links.
IMAGE_FACEDESK = "https://media.tumblr.com/tumblr_lqegp8wjxZ1qktqch.gif"
IMAGE_LMLU = "https://68.media.tumblr.com/tumblr_mej070O7Lj1qktqch.gif"
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
               "http://safebooru.org//images/2048/60ce6f6888ba2fce6393638223dcc8d7c67f0655.jpg",
               "https://i.giphy.com/xT1XGLm7CJknNZKVS8.gif")
IMAGES_GLOMP = ("http://safebooru.org/images/1575/8e2b95aefa17208aa5b5bc2aa687a8d791adf20a.gif",
                "http://safebooru.org/images/1860/e8562c569fb94477671947ad96a0b88ac999569a.gif",
                "http://safebooru.org/images/579/cd1913e6aaa91bb3abb752ebd9fb410099396acd.gif",
                ("http://safebooru.org/samples/2095/"
                 "sample_c1fc61605ea086c339d0b8376efbfb83003d1a96.jpg"))
IMAGES_IDK = ("http://safebooru.org/images/1513/6198de35cc3a7ffb2bd5cd46a89ca91fb117b3db.gif",
              "http://safebooru.org/images/2098/bbe8b8f0fc5b630133d10a16bbeb29b81d64db50.jpg",
              "http://safebooru.org/images/1977/e3988fa3bb6125f77b8e55d648ab1aebdd317bc7.jpg",
              "http://safebooru.org/samples/1768/sample_2bf2f0acc1c06e34deef043066ebb17c21de4238.jpg",
              "http://safebooru.org/images/937/ae704e58e0d58ddf57d3793609f9994a2b831301.jpg")
IMAGES_WAGGING = ("http://safebooru.org//images/146/78639fe8edd6cb75a0f031b4dfb0773fdda6b4e8.jpg",
                  "http://safebooru.org//images/763/2136ae257bb49f34552070d566b9eb23884a48c4.jpg",
                  "http://safebooru.org//images/599/7fc582995b8fa21555791bfed382f0f634ca3cbb.jpg",
                  "http://safebooru.org//images/275/3c5368c8f7bd3795052ce38ae860c9fa4b97f473.gif",
                  "http://safebooru.org//images/1990/96b8cf2274c20df69c3ba04d4a3a6647cb07a3f0.gif",
                  "http://safebooru.org//images/824/c271151ac920b664ed4de06d9770199f6d16d70f.gif",
                  "http://safebooru.org//images/906/fae7d69ba34b74795546d58b322d33189fce8418.gif",
                  "http://safebooru.org//images/1428/f5bcb191dfdd0881db66eb676b9f42df214629b0.gif",
                  "http://safebooru.org//images/1891/5922d9fe102f8b2e62b2761eb505ee75fdcde2df.gif",
                  "http://safebooru.org//images/1853/10962bdb8ffeda856e15882593788cd09e58ee2e.gif")
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
IMAGES_LICK = ("http://safebooru.org/images/189/0a412d1db7f53cd2505df9cf16be693dcac0855b.jpeg",
               "http://safebooru.org/images/358/f64d461f47319d8dae9adb899c0de24fca70127d.png",
               "http://safebooru.org/images/2116/4b8cf6a3f4cd38a610697df4f0fe1074e67070af.jpg")
IMAGES_POKE = ("http://safebooru.org/images/1880/e3b020472d86b0a04ffec8cdf41049ef66cf3a68.gif",
               "http://safebooru.org/images/2051/031566980728255e6d7e2fba8c12a3c38ea7598a.gif",
               "http://safebooru.org/images/1169/3edae332d38c887a8723207d1bc0dffac8244591.gif")
IMAGES_SANDWICHES = ("https://i.imgur.com/kyTDwIX.png",
                     "https://i.imgur.com/ULKlVhU.png",
                     "https://i.imgur.com/Z2RvlBx.png",
                     "https://i.imgur.com/k5GnTbU.png",
                     "https://i.imgur.com/SzuegH9.png",
                     "https://i.imgur.com/ppcHtKd.png",
                     "https://i.imgur.com/xy8iwN5.png")
IMAGES_KONKON = ("http://safebooru.org/images/1856/6e6b3319f2a0a3fe5e77567ebdc998b3c4cb3900.jpg",
                 "http://safebooru.org/samples/1832/sample_25adf8a37226fa003a6a6d7b0f3171f5764bba7d.jpg",
                 "http://safebooru.org/images/1270/a9c1744fb4676f743c4dbc7668a39e72decdde16.jpg",
                 "http://safebooru.org/images/2077/12bddb7bd2274f0ba9abe2d72c994555d562e0df.jpg",
                 ("http://safebooru.org/samples/2045/"
                  "sample_c2a906de7bf13b48c7c971e909f1beef75766c34.png"))
IMAGES_WHAT = ("https://media.tumblr.com/tumblr_lnvtzjiY4J1qktqch.png",
               "https://owo.whats-th.is/a740f1.png",
               "http://media.tumblr.com/tumblr_lpob17Ru5v1qktqch.gif")

class Reactions:
    """Weeb reaction commands."""

    def _generate_message(self, ctx, kind:str=None, member:discord.Member=None):
        """Generate a message based on the member."""
        if not kind or not member:
            message=""
        elif ctx.bot.user.id == member.id:
            message=f"Aw, thank you. Here, have one back. :3"
        elif ctx.author.id != member.id:
            message=f"**{member.display_name}**, you got a {kind} from **{ctx.author.display_name}!**"
        else:
            message=f"**{member.display_name}**, I'm so sorry. Have a {kind} anyway. :<"
        return message

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
                url_image = BASE_URL_IMAGE.format(data).replace("i/", "")
                message = self._generate_message(ctx, kind, member)
                if not helpers.has_scanning(ctx):
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

    async def _send_image(self, ctx, url_image, kind:str=None, member:discord.Member=None):
        """A helper function that creates an embed with an image and sends it off."""
        if isinstance(url_image, (tuple, list)):
            url_image = systemrandom.choice(url_image)
        message = self._generate_message(ctx, kind, member)
        if not helpers.has_scanning(ctx):
            embed = discord.Embed(color=utils.random_color())
            embed.set_image(url=url_image)
            await ctx.send(message, embed=embed)
        else:
            message = "\n".join([str(message), url_image])
            await ctx.send(message)

    # Commands based on _send_image()
    @commands.command(aliases=["rip"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def dead(self, ctx):
        """Dead!"""
        await self._send_image(ctx, IMAGES_DEAD)

    @commands.command(aliases=["facedesk"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def fdesk(self, ctx):
        """Facedesk!"""
        await self._send_image(ctx, IMAGE_FACEDESK)

    @commands.command(aliases=["tacklehug", "tackle"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def glomp(self, ctx, *, member:discord.Member):
        """Glomp!"""
        await self._send_image(ctx, IMAGES_GLOMP, "glomp", member)

    @commands.command(aliases=["idek"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def idk(self, ctx):
        """IDK!"""
        await self._send_image(ctx, IMAGES_IDK)

    @commands.command(aliases=["konkon"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def kon(self, ctx):
        """Kon, kon!"""
        await self._send_image(ctx, IMAGES_KONKON)

    @commands.command(aliases=["lmly", "letmeloveyou"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def lmlu(self, ctx):
        """Let me love you!"""
        await self._send_image(ctx, IMAGE_LMLU)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def poke(self, ctx, *, member:discord.Member):
        """Poke!"""
        await self._send_image(ctx, IMAGES_POKE, "poke", member)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def what(self, ctx):
        """What?"""
        await self._send_image(ctx, IMAGES_WHAT)

    @commands.command(aliases=["idu", "ideu", "wakarimasenlol"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def wlol(self, ctx):
        """Wakarimasen, lol!"""
        await self._send_image(ctx, IMAGE_WLOL)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def boots(self, ctx):
        """Boots!"""
        await self._send_image(ctx, IMAGES_BOOTS)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def sandwich(self, ctx):
        """Sandwich!"""
        await self._send_image(ctx, IMAGES_SANDWICHES)

    @commands.command(aliases=["tailwag"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def wag(self, ctx):
        """Tail wag!"""
        await self._send_image(ctx, IMAGES_WAGGING)

    # Commands based on _rra()
    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def cry(self, ctx):
        """Cry!"""
        await self._rra(ctx, "cry")

    @commands.command(aliases=["snuggle"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def cuddle(self, ctx, *, member:discord.Member):
        """Cuddle a member!
        
        * member - The member to be cuddled."""
        await self._rra(ctx, "cuddle", member)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def hug(self, ctx, *, member:discord.Member):
        """Hug a member!
        
        * member - The member to be hugged."""
        await self._rra(ctx, "hug", member)
        
    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def kiss(self, ctx, *, member:discord.Member):
        """Kiss a member!
        
        * member - The member to be kissed."""
        await self._rra(ctx, "kiss", member)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def lewd(self, ctx):
        """Lewd!"""
        choice = bool(systemrandom.getrandbits(1))
        if choice:
            await self._rra(ctx, "lewd")
        else:
            await self._send_image(ctx, IMAGES_LEWD)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def lick(self, ctx, *, member:discord.Member):
        """Lick a member!
        
        * member - The member to be licked."""
        if hasattr(ctx.channel, "is_nsfw") and ctx.channel.is_nsfw():
            await self._rra(ctx, "lick", member)
        else:
            await self._send_image(ctx, IMAGES_LICK, "lick", member)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def nom(self, ctx):
        """Nom!"""
        await self._rra(ctx, "nom")

    @commands.command(aliases=['nya', 'meow'])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def nyan(self, ctx):
        """Nyan!"""
        await self._rra(ctx, "nyan")

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def owo(self, ctx):
        """owo"""
        await self._rra(ctx, "owo")

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def pat(self, ctx, *, member:discord.Member):
        """Pat a member!
        
        * member - The member to be patted."""
        await self._rra(ctx, "pat", member)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def pout(self, ctx):
        """Pout!"""
        await self._rra(ctx, "pout")

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def slap(self, ctx, *, member:discord.Member):
        """Slap a member!
        
        * member - The member to be slapped."""
        await self._rra(ctx, "slap", member)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def smug(self, ctx):
        """Smug!"""
        await self._rra(ctx, "smug")

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def stare(self, ctx, *, member:discord.Member):
        """Stare at a member!
        
        * member - The member to be stared at."""
        await self._rra(ctx, "stare", member)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def tickle(self, ctx, *, member:discord.Member):
        """Tickle a member!
        
        * member - The member to be tickled."""
        await self._rra(ctx, "tickle", member)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def triggered(self, ctx):
        """Triggered!"""
        await self._rra(ctx, "triggered")

def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Reactions())
