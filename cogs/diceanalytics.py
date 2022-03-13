import discord
from discord.ext import commands
import json
import os
import random
import re
import sys

from typing import List, Dict, Union, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

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

            
        
    @commands.command(aliases=["da","diceanal"])
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
            return str(s.replace("[","").replace("]",""))

        with open("dicelogs.json", "r") as f:
            SESSION_RESULTS = json.load(f)

        for user_log in SESSION_RESULTS:
            for log in SESSION_RESULTS[user_log]:
                diceroll = [int(strip(dr)) for dr in log[3].split(",")]
                for dr in diceroll:
                    DICE_DISTRIBUTION[str(dr)] += 1
        embed = discord.Embed()
        
        DICE_DISTRIBUTION = sorted(DICE_DISTRIBUTION, key=lambda x: x[0])
        
        embed.add_field(name="Dice Analytics", value="\u200b", inline=False)
        embed.add_field(name="Dice", value="\u200b", inline=True)
        embed.add_field(name="Value", value="\u200b", inline=True)
        message = []
        for key, value in enumerate(DICE_DISTRIBUTION):
            message.append(f"""{key} .................. {value}""")
        message_string = "\n".join(message)    
        embed.add_field(name=f"{message_string}", value=f"\u200b", inline=False)
        await ctx.send(embed=embed)
        return




def setup(client):
    client.add_cog(DiceAnalytics(client))