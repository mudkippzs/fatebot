import discord
from discord.ext import commands
import asyncio

import json
import random
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger
from split_text import split_text

with open("config.json", "r") as f:
    config = json.load(f)


class botstatusmanager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["status_rotate", "rotate_status", "statusrotate", "rotatestatus"])
    async def statrot(self, ctx):  # pylint: disable=unused-argument; command is used in on_ready event handler below instead of directly by user (see main)

        """Rotates the bots status message between a list of status messages."""
        if str(ctx.author.id) not in [config["gamemaster"][0]["ganj"]]:
            await ctx.send("```You can't use this command.```", delete_after=5.0)

        await self._status_rotate()  # pylint: disable=no-value-for-parameter; _status_rotate takes no arguments but is called with one due to use as an event handler (see main)

    @commands.Cog.listener()
    async def on_ready(self):
        await self._status_rotate()

    @commands.Cog.listener()
    async def _status_rotate(self):  # pylint: disable=unused-argument; _status_rotate takes no arguments but is called with one due to use as an event handler (see main)

        """Rotates the bots status message between a list of status messages."""

        # wait until bot has logged in and initialised before running code
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():  # loop forever until bot closes
            status_list = [
                ('the future...', discord.ActivityType.watching),
                ('the logs of fate...', discord.ActivityType.watching),
                ('with the laws of nature...', discord.ActivityType.playing),
                ('dice with God...', discord.ActivityType.playing),
                ('the sands of time...', discord.ActivityType.watching),
                ('with entropy...', discord.ActivityType.playing),
                ('you...', discord.ActivityType.watching)]

            random.shuffle(status_list)

            for status in status_list:  # iterate through each item in the list, setting the bots status message to each item sequentially
                # change the bots presence by setting its activity attribute to a discord Game object containing our new status message
                await self.bot.change_presence(activity=discord.Activity(name=status[0], type=status[1]))
                # sleep for 5 seconds before moving on to next iteration of loop
                await asyncio.sleep(600)


def setup(bot):  # function necessary for loading cogs by calling bot.add_cog() within this function
    bot.add_cog(botstatusmanager(bot))
