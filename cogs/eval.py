#!/usr/bin/env python3

# Standard modules
import logging
import subprocess

# Third party modules
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Evaluation:
    """Commands that evaluate commands.."""
    
    @commands.command()
    @commands.is_owner()
    async def sh(self, ctx, *, command):
        """Execute a system command. Bot owner only."""
        command = command.split(" ")
        process = subprocess.Popen(command,
                                   universal_newlines=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        try:
            output, errors = process.communicate(timeout=8)
            output = output.split("\n")
            process.terminate()
        except subprocess.TimeoutExpired:
            process.kill()
            output = ["Command timed out. x.x"]
        paginator = commands.Paginator(prefix="```bash")
        for line in output:
            paginator.add_line(line)
        for page in paginator.pages:
            await ctx.send(page)
        string_output = "\n".join(output)
        logger.info(f"Execution of {expression} complete. Output:\n{string_output}")

    @commands.command(name="eval")
    @commands.is_owner()
    async def _eval(self, ctx, *, expression):
        """Evaluate a Python expression. Bot owner only."""
        try:
            output = eval(expression)
            output = str(output).split("\n")
        except Exception as error:
            output = [f"x.x An error has occurred: {error}"]
        paginator = commands.Paginator(prefix="```py")
        for line in output:
            paginator.add_line(line)
        for page in paginator.pages:
            await ctx.send(page)
        string_output = "\n".join(output)
        logger.info(f"Evaluation of {expression} complete. Output:\n{string_output}")
    
def setup(bot):
    """Setup function for evaluation."""
    bot.add_cog(Evaluation())
