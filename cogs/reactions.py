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
BASE_URL_IMAGE = "https://cdn.ram.moe{0[path]}"

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
               "http://safebooru.org/images/2048/60ce6f6888ba2fce6393638223dcc8d7c67f0655.jpg",
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
IMAGES_WAGGING = ("http://safebooru.org/images/146/78639fe8edd6cb75a0f031b4dfb0773fdda6b4e8.jpg",
                  "http://safebooru.org/images/763/2136ae257bb49f34552070d566b9eb23884a48c4.jpg",
                  "http://safebooru.org/images/599/7fc582995b8fa21555791bfed382f0f634ca3cbb.jpg",
                  "http://safebooru.org/images/275/3c5368c8f7bd3795052ce38ae860c9fa4b97f473.gif",
                  "http://safebooru.org/images/1990/96b8cf2274c20df69c3ba04d4a3a6647cb07a3f0.gif",
                  "http://safebooru.org/images/824/c271151ac920b664ed4de06d9770199f6d16d70f.gif",
                  "http://safebooru.org/images/906/fae7d69ba34b74795546d58b322d33189fce8418.gif",
                  "http://safebooru.org/images/1428/f5bcb191dfdd0881db66eb676b9f42df214629b0.gif",
                  "http://safebooru.org/images/1891/5922d9fe102f8b2e62b2761eb505ee75fdcde2df.gif",
                  "http://safebooru.org/images/1853/10962bdb8ffeda856e15882593788cd09e58ee2e.gif",
                  ("http://68.media.tumblr.com/01e9cc48310fbe72b2ccf1b52925d0c4/"
                   "tumblr_o3at2et2G31tydz8to1_540.gif"),
                  ("https://lh3.googleusercontent.com/-rrPLI80iYmw/VQbtiyQhFwI/"
                   "AAAAAAAA9Pg/XUGGf7yT6CY/w500-h273/tumblr_mmeanbZFmO1qg78wpo1_500.gif"),
                  ("http://24.media.tumblr.com/a1d0298a6c2e7821ed102ad2345fcc4a/"
                   "tumblr_myauniO7nO1r0wlweo1_500.gif"),
                  "http://i.imgur.com/MSCtuve.gif",
                  ("https://38.media.tumblr.com/8203abcf4aef7f528eb61206710bfdce/"
                   "tumblr_nnwn56DQuR1ty38iao1_400.gif"),
                  ("https://68.media.tumblr.com/c54e506582785a3e89d223fa3dba2fd6/"
                   "tumblr_nyman1FuBi1tydz8to1_500.gif"))
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
               "https://i.imgur.com/rWLoIzf.png",
               "https://secure.static.tumblr.com/753b4405d4c926ef8224e3ac5ec30aef/f52giag/4Uin6xuha/tumblr_static_tumblr_static_2p47ogg0mhus4gs8skwwcc8sw_640.gif")
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
IMAGES_WAVE = ("http://safebooru.org/images/2131/321680e22202367aebff73781458612269699518.jpg",
               "http://safebooru.org/images/531/94bee4c0ba0055eb531893c2b0b231e809b6a885.png",
               "http://safebooru.org/images/540/73530f81c9a2675df3ceb0faf0d4a6f97478b8a2.jpg",
               "http://safebooru.org/images/1753/93b7b450403c2d08cb73429356725242124fe5aa.png",
               "http://safebooru.org/images/1818/f9286e77a04f547d8da89349ebbdae8ad40286c0.jpg")
IMAGES_WHAT = ("https://media.tumblr.com/tumblr_lnvtzjiY4J1qktqch.png",
               "https://owo.whats-th.is/a740f1.png",
               "http://media.tumblr.com/tumblr_lpob17Ru5v1qktqch.gif")

class Reactions:
    """Weeb reaction commands."""

    def _generate_message(self, ctx, kind:str=None, user:discord.Member=None):
        """Generate a message based on the user."""
        if not kind or not user:
            message=""
        elif ctx.bot.user.id == user.id:
            message=f"Aw, thank you. Here, have one back. :3"
        elif ctx.author.id != user.id:
            message=f"**{user.display_name}**, you got a {kind} from **{ctx.author.display_name}!**"
        else:
            message=f"**{user.display_name}**, I'm so sorry. Have a {kind} anyway. :<"
        return message

    async def _rra(self, ctx, kind:str, user:discord.Member=None):
        """A helper function that grabs an image and posts it in response to a user.
        
        * kind - The type of image to retrieve.
        * user - The member to mention in the command."""
        logger.info(f"Fetching {kind} image.")
        hash_id_channel = utils.to_hash(str(ctx.channel.id))
        url = BASE_URL_API.format(kind)
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                url_image = BASE_URL_IMAGE.format(data).replace("i/", "")
                message = self._generate_message(ctx, kind, user)
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

    async def _send_image(self, ctx, url_image, kind:str=None, user:discord.Member=None):
        """A helper function that creates an embed with an image and sends it off."""
        if isinstance(url_image, (tuple, list)):
            url_image = systemrandom.choice(url_image)
        message = self._generate_message(ctx, kind, user)
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
    async def glomp(self, ctx, *, user:discord.Member):
        """Glomp!"""
        await self._send_image(ctx, IMAGES_GLOMP, "glomp", user)

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

    @commands.command(aliases=["boop"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def poke(self, ctx, *, user:discord.Member):
        """Poke!"""
        await self._send_image(ctx, IMAGES_POKE, "poke", user)

    @commands.command(aliases=["waving"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def wave(self, ctx):
        """Wakarimasen, lol!"""
        await self._send_image(ctx, IMAGES_WAVE)

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
    async def cuddle(self, ctx, *, user:discord.Member):
        """Cuddle a user!
        
        * user - The user to be cuddled."""
        await self._rra(ctx, "cuddle", user)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def hug(self, ctx, *, user:discord.Member):
        """Hug a user!
        
        * user - The user to be hugged."""
        await self._rra(ctx, "hug", user)
        
    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def kiss(self, ctx, *, user:discord.Member):
        """Kiss a user!
        
        * user - The user to be kissed."""
        await self._rra(ctx, "kiss", user)

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
    async def lick(self, ctx, *, user:discord.Member):
        """Lick a user!
        
        * user - The user to be licked."""
        if hasattr(ctx.channel, "is_nsfw") and ctx.channel.is_nsfw():
            await self._rra(ctx, "lick", user)
        else:
            await self._send_image(ctx, IMAGES_LICK, "lick", user)

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
    async def pat(self, ctx, *, user:discord.Member):
        """Pat a user!
        
        * user - The user to be patted."""
        await self._rra(ctx, "pat", user)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def pout(self, ctx):
        """Pout!"""
        await self._rra(ctx, "pout")

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def slap(self, ctx, *, user:discord.Member):
        """Slap a user!
        
        * user - The user to be slapped."""
        await self._rra(ctx, "slap", user)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def smug(self, ctx):
        """Smug!"""
        await self._rra(ctx, "smug")

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def stare(self, ctx, *, user:discord.Member):
        """Stare at a user!
        
        * user - The user to be stared at."""
        await self._rra(ctx, "stare", user)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def tickle(self, ctx, *, user:discord.Member):
        """Tickle a user!
        
        * user - The user to be tickled."""
        await self._rra(ctx, "tickle", user)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def triggered(self, ctx):
        """Triggered!"""
        await self._rra(ctx, "triggered")

def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Reactions())
