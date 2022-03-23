"""
1. Create a discord cog that allows users to set their timezone.
2. Save the timezone in a json file.
3. When a message is sent that contains a date or time string, add a clock emoji.
4. When a member reacts to the clock emoji, DM them the time or date converted to their local time in a DM.
"""

import asyncio
import datetime
import json
import logging
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from timefhuman import timefhuman

import discord
from discord.ext import commands
from pytz import timezone as pytz_timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger

class Timefriend(commands.Cog):
    """A cog for setting and converting timezones."""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("timefriendlog")
        self.tz_file = "data/timefriend/settings.json"
        self.tz_emoji = "\N{MANTELPIECE CLOCK}"
        self.tz_emoji_name = ":clock:"
        self.tz_emoji_regex = re.compile(rf":{self.tz_emoji_name}:")
        self.tz_emoji_regex_str = f":{self.tz_emoji_name}:"
        self.tz_emoji_regex_str_escaped = re.escape(self.tz_emoji_regex_str)
        self.tz_emoji_regex_escaped = re.compile(rf":{self.tz_emoji_name}:")
        self.tz_local = ZoneInfo("Europe/Amsterdam")
        self.tz_local_name = self.tz_local
        self.tz_local_offset = self.tz_local.utcoffset(datetime.now())
        self.tz_local_offset = (
            f"{self.tz_local_offset.days * 24 + self.tz_local_offset.seconds // 3600:+03}"
        )
        
        self.load() # load TZ db.

    def load(self):
        """Load the timezone data from the json file."""
        if os.path.isfile(self.tz_file):
            with open(self.tz_file, "r") as f:
                self.tz_data = json.load(f)
            clogger("TZ DB loaded.")
            #clogger(self.tz_data)
        else:
            clogger("Couldn't load TZ DB.")

    def save(self):
        """Save the timezone data to the json file."""
        with open(self.tz_file, "w") as f:
            json.dump(self.tz_data, f)

    @commands.command(name="timezone", aliases=["tz"])
    async def timezone(self, ctx, *, tz: str = None):
        """Set your timezone."""
        if str(ctx.message.guild.id) not in self.tz_data.keys():
            self.tz_data[str(ctx.message.guild.id)] = {}

        if tz is None:
            if str(ctx.author.id) in self.tz_data[str(ctx.message.guild.id)]:
                tz = self.tz_data[str(ctx.message.guild.id)][str(ctx.author.id)]
                await ctx.send(f"Your timezone is set to {tz}.")
            else:
                await ctx.send("You have not set a timezone.")
        else:
            try:
                pytz_timezone(tz)
            except Exception as e:
                self.logger.error(e)
                await ctx.send("That is not a valid timezone.")
            else:
                self.tz_data[str(ctx.message.guild.id)][str(ctx.author.id)] = tz
                self.save()
                await ctx.send(f"Your timezone has been set to {tz}.")

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Send a DM to the user when they react to the clock emoji."""
        if payload.emoji.name != "🕰":
            return

        user = self.bot.get_user(payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.author == self.bot.user or user.bot:
            return

        datestring = timefhuman(message.clean_content)
        if datestring:

            if user is None:
                return

            clogger(self.tz_data)
            clicker_tz = self.tz_data[str(message.guild.id)][str(user.id)] if str(user.id) in self.tz_data[str(message.guild.id)].keys() else self.tz_local_name
            author_tz = self.tz_data[str(message.guild.id)][str(message.author.id)] if str(message.author.id) in self.tz_data[str(message.guild.id)].keys() else self.tz_local_name
            
            clicker_tz = pytz_timezone(str(clicker_tz))
            author_tz = pytz_timezone(str(author_tz))

            dt = author_tz.localize(datestring)

            dt_local = dt.astimezone(clicker_tz)

            await user.send(f"{dt.strftime('%A %d %B %Y at %H:%M')} in {author_tz.zone} is {dt_local.strftime('%A %d %B %Y at %H:%M')} in {clicker_tz.zone}.")
        

    @commands.Cog.listener()
    async def on_message(self, payload):
        """Add the clock emoji to messages that contain a date or time."""
        if payload.author == self.bot.user:
            return

        try:
            datestring = timefhuman(payload.clean_content)
            if datestring:
                pass
                #await payload.add_reaction(self.tz_emoji)
        except (ValueError, AssertionError):
            pass

def setup(bot):
    """Add the cog to the bot."""
    bot.add_cog(Timefriend(bot))