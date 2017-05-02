#!/usr/bin/env python3

import logging

from discord.ext import commands

DIGITS_MAX = 16

class Temperature:

    @commands.command(name="f2c")
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def fahrenheit_to_celsius(self, ctx, temperature:float):
        """Convert temperature in Fahrenheit to Celsius.
        
        * temperature - An integer representing temperature in Fahrenheit."""
        if len(str(temperature)) > DIGITS_MAX:
            raise commands.UserInputError("Too long.")
        fahrenheit = round(temperature, 3)
        celsius = round((temperature - 32) * 5/9, 3)
        await ctx.send(f"{fahrenheit} Fahrenheit = {celsius} Celsius")

    @commands.command(name="c2f")
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def celsius_to_fahrenheit(self, ctx, temperature:float):
        """Convert temperature in Celsius to Fahrenheit.
        
        * temperature - An integer representing temperature in Celsius."""
        if len(str(temperature)) > DIGITS_MAX:
            raise commands.UserInputError("Too long.")
        celsius = round(temperature, 3)
        fahrenheit = round((temperature * 9/5) + 32, 3)
        await ctx.send(f"{celsius} Celsius = {fahrenheit} Fahrenheit")

def setup(bot):
    """Setup function."""
    bot.add_cog(Temperature())
