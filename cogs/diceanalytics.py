import discord
from discord.ext import commands
import json
import os
import random
import re
import sys

from typing import List, Dict, Union, Optional

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger
from split_text import split_text


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)


class DiceAnalytics(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["da", "diceanal"])
    async def diceanalytics(self, ctx):
        """Show the distribution of dice rolls."""

        DICE_DISTRIBUTION = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0,
            "10": 0,
        }

        def strip(s):
            return str(s.replace("[", "").replace("]", ""))

        with open("dicelogs.json", "r") as f:
            SESSION_RESULTS = json.load(f)

        for user_log in SESSION_RESULTS:
            for log in SESSION_RESULTS[user_log]:
                diceroll = log[3].replace("[", "").replace("]", "").split(",")
                if len(diceroll):
                    if len(diceroll[0]):
                        for dr in diceroll:
                            DICE_DISTRIBUTION[str(dr)] += 1
        embed = discord.Embed(title="Dice Roll Analysis - Result Frequency")

        clogger(DICE_DISTRIBUTION)
        embed.add_field(
            name="\u200b", value="```Result             Frequency```", inline=True)
        for key in DICE_DISTRIBUTION:
            embed.add_field(
                name=f"\u200b", value=f"```{key:<20}{DICE_DISTRIBUTION[key]:>6}```", inline=False)
        await ctx.send(embed=embed)
        return


def setup(client):
    client.add_cog(DiceAnalytics(client))
