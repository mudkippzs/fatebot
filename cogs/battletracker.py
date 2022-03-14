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
from npc import NPC
from player import Player
from split_text import split_text


with open("config.json", "r") as f:
    config = json.load(f)


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)


def get_encounter():
    return


def random_encounter():

    encounter = {
        "civilians": [

        ],
        "creatures": [],
        "peon": [],
        "grunts": [],
        "miniboss": [],
        "boss": [],
        "bigboss": [],
        "deadly": [],
    }

    return encounter


class BattleEngine(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["commands"])
    async def create_encounter(self, ctx, encounter_id=0):
        if encounter_id > 0:
            encounter = get_encounter(encounter_id)
        else:
            encounter = random_encounter()

        player_list = ", ".join([p.display_name for p in ctx.message.mentions])
        await ctx.send(f"```Starting a battle with {len(ctx.message.mentions)}"
                       f"players: {player_list}```")


def setup(client):
    client.add_cog(BattleEngine(client))
