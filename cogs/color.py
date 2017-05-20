#!/usr/bin/env python3

"""Contains a cog that fetches colors."""

# Standard library
import random

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
import helpers

BASE_URL_COLOURLOVERS_API = "http://www.colourlovers.com/img/{0}/80/80/{0}.png"
BASE_URL_TINEYE_MULTICOLR = "http://labs.tineye.com/multicolr/#colors={0};weights=100"
BASE_URL_COLOR_HEX = "http://www.color-hex.com/color/{0}"

systemrandom = random.SystemRandom()

class Color:
    """Color command."""
    
    @commands.command(aliases=["colour"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def color(self, ctx, *, color:str=None):
        """Display a color.
        
        * color - This represents a color. Accepts hex input."""
        try:
            if color:
                color = color.lstrip("#") # Remove the pound sign.
                color = int(f"0x{color}", 16)
            else:
                color = systemrandom.randint(0, 16777215)
            color = discord.Color(color)
        except ValueError:
            raise commands.UserInputError(("Not a valid color. "
                                           "Color must be in hex format (e.g. `808080`) "
                                           "and must be between `FFFFFF` and `000000`."))
        
        color_hex_value = "%0.2X%0.2X%0.2X" % (color.r, color.g, color.b)
        
        embed = discord.Embed()
        embed.color = color
        image_url = BASE_URL_COLOURLOVERS_API.format(color_hex_value)
        if not helpers.has_scanning(ctx):
            embed.set_thumbnail(url=image_url)
        else:
            embed.set_footer(text="Thumbnail omitted on this channel due to image scanning.")
        embed.add_field(name="RGB", value=f"{color.to_rgb()}")
        embed.add_field(name="Hex code", value=f"#{color_hex_value}")
        embed.add_field(name="Images",
                        value=BASE_URL_TINEYE_MULTICOLR.format(color_hex_value.lower()))
        embed.add_field(name="Information",
                        value=BASE_URL_COLOR_HEX.format(color_hex_value.lower()))
        await ctx.send(embed=embed)
        
        if helpers.has_scanning(ctx):
            await message.delete()

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Color())
