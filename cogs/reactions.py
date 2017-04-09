#!/usr/bin/env python3

"""Contains a cog for reaction image commands."""

# Standard modules
import logging
import random

# Third-party modules
import discord
from discord.ext import commands

# Bundled modules
import utils
import helpers

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

logger = logging.getLogger(__name__)

class Fun:
    """discord.py cog containing reaction image functions of the bot."""
    def __init__(self):
        pass

    async def send_image(self, ctx, url_image):
        """A helper function that just creates an embed with an image and sends it off."""
        embed = discord.Embed(color=utils.random_color())
        if isinstance(url_image, tuple):
            embed.set_image(url=random.choice(url_image))
        elif isinstance(url_image, str):
            embed.set_image(url=url_image)
        else:
            embed.description = str(url_image)
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def kys(self, ctx):
        """Ask the bot to kill itself."""
        await ctx.send("That's mean. :<")

    @commands.command()
    async def dead(self, ctx):
        """Display dead chat reaction image."""
        await self.send_image(ctx, IMAGE_DEAD)

    @commands.command(aliases=["facedesk"])
    async def fdesk(self, ctx):
        """Display facedesk reaction image."""
        await self.send_image(ctx, IMAGE_FACEDESK)

    @commands.command(aliases=["letmeloveyou"])
    async def lmly(self, ctx):
        """Display "let me love you" reaction image."""
        await self.send_image(ctx, IMAGE_LMLY)

    @commands.command()
    async def what(self, ctx):
        """Display WHAT reaction image."""
        await self.send_image(ctx, IMAGE_WHAT)

    @commands.command(aliases=["wakarimasenlol"])
    async def wlol(self, ctx):
        """Display "Wakarimasen, lol" reaction image."""
        await self.send_image(ctx, IMAGE_WLOL)

    @commands.command()
    async def boots(self, ctx):
        """Display images of anime boots."""
        await self.send_image(ctx, IMAGES_BOOTS)

    @commands.command()
    async def sandwich(self, ctx):
        """Display a sandwich."""
        await self.send_image(ctx, IMAGES_SANDWICHES)

def setup(bot):
    """Setup function for Reactions."""
    bot.add_cog(Fun())
