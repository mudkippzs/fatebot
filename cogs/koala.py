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

def get_koala():
    koala = None
    url = "https://some-random-api.ml/animal/koala"

    response = requests.get(url)

    koala = response.json()

    return koala

class Koalas(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(aliases=["koala"])
    async def koalas(self, ctx):
        embed = discord.Embed(title=f"\u200b", timestamp=ctx.message.created_at)
        koala_data = get_koala()
        embed.set_image(url=koala_data["image"])
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        fact = f"...{koala_data['fact'][0].lower()}{koala_data['fact'][1:]}"
        embed.add_field(name=f"{ctx.author.display_name} did you know...", value=f"```{fact}```")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Koalas(client))