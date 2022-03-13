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

class Moderation(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot        
    
    @commands.command(aliases=["purgemessages"])
    async def purge(ctx, limit: int, member: discord.Member = None):
        """Owner only - Delete messages from a channel."""
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:
            if member is None:
                await ctx.channel.purge(limit=limit)
            else:
                await ctx.channel.purge(limit=limit, check=lambda m: m.author == member)
        else:
            await ctx.send("```Sorry, only the owner can purge messages.```", delete_after=5.0)


def setup(client):
    client.add_cog(Moderation(client))