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

with open("config.json", "r") as f:
    config = json.load(f)

def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)

class Immersion(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["shieldsmokes","shieldcig","shieldcigs"])
    async def shieldsmoke(self, ctx):
        """A shield belonging to Leonidas of Sparta, it has a cigarette case attached which is always half full. When any cigarette is drawn, it is of a random brand deicded at the time it's taken."""
        cigarette_brands = config["brands"].split(",")
        
        if str(ctx.message.author.id) not in [config["gamemaster"][0]["ganj"], config["players"][0]["vasily"]]:
            await ctx.send("```You are not Vasily, only Vasily can smoke Vasily's smokes...```", delete_after=5.0)
        else:
            if str(ctx.message.author.id) == config["players"][0]["vasily"]:
                vasily = "```Vasily opens his"
            else:
                vasily = f"```{ctx.message.author.display_name} opens Vasily's"
            
            if ctx.message.mentions: 
                target = ctx.message.mentions[0].display_name
                await ctx.send(f"{vasily} divine cigarette case and pulls a [{random.choice(cigarette_brands)}] and passes it to {target}```")
            else:            
                await ctx.send(f"{vasily} divine cigarette case and pulls a [{random.choice(cigarette_brands)}]```")


def setup(client):
    client.add_cog(Immersion(client))