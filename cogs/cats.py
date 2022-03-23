import discord
from discord.ext import commands
import json
import os
import random
import re
import requests
import sys

from typing import List, Dict, Union, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger
from split_text import split_text

with open("config.json", "r") as f:
    config = json.load(f)

def get_cat():
    cat = None
    api_key = config["cats_api_key"]
    url = "https://api.thecatapi.com/v1/images/search"

    headers = {'x-api-key': api_key}
    response = requests.get(url, headers=headers)

    cat = response.json()[0]

    return cat

class Cats(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(aliases=["commands"])
    async def cats(self, ctx):
        embed = discord.Embed(title=f"{ctx.author.display_name} requested a cat...", timestamp=ctx.message.created_at)
        cat_data = get_cat()
        embed.set_image(url=cat_data["url"])

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Cats(client))