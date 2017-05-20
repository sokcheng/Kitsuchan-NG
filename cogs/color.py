#!/usr/bin/env python3

"""Contains a cog that fetches colors."""

# Standard library
import random

# Third party modules
import discord
from discord.ext import commands

# Bundled modules
import helpers

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
        
        if helpers.has_scanning(ctx):
            message = await ctx.send("Waiting on image scanning to complete... -.-;")
        
        color_hex_value = "%0.2X%0.2X%0.2X" % (color.r, color.g, color.b)
        
        embed = discord.Embed()
        embed.color = color
        image_url = f"http://www.colourlovers.com/img/{color_hex_value}/128/128/{color_hex_value}.png"
        embed.set_thumbnail(url=image_url)
        embed.add_field(name="RGB", value=f"{color.to_rgb()}")
        embed.add_field(name="Hex code", value=f"#{color_hex_value}")
        await ctx.send(embed=embed)
        
        if helpers.has_scanning(ctx):
            await message.delete()

def setup(bot):
    """Setup function for Utilities."""
    bot.add_cog(Color())
