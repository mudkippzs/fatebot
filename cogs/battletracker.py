from npc import NPC

import json
import os
import random
import re
import sys

import discord
from discord.ext import commands

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from battlewheel import Battle
from clogger import clogger
from player import Player


with open("config.json", "r") as f:
    config = json.load(f)


def strip_tags(string):
    """
    This function will strip all html tags from string
    returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)


def get_encounter():
    return


def random_encounter():

    encounter = {
        "civilians": [

        ],
        "creatures": [],
        "peons": [],
        "grunts": [],
        "miniboss": [],
        "boss": [],
        "bigboss": [],
        "deadly": [],
    }

    for _ in range(10):
        encounter["civilians"].append(NPC(legend=0, debug=True))

    for _ in range(6):
        encounter["grunts"].append(
            NPC(legend=random.randint(1, 2), debug=True))

    for _ in range(4):
        encounter["peons"].append(NPC(legend=random.randint(0, 1), debug=True))

    for _ in range(3):
        encounter["miniboss"].append(
            NPC(legend=random.randint(3, 5), debug=True))

    for _ in range(3):
        encounter["boss"].append(NPC(legend=random.randint(4, 6), debug=True))

    for _ in range(3):
        encounter["bigboss"].append(
            NPC(legend=random.randint(6, 7), debug=True))

    for _ in range(3):
        encounter["deadly"].append(
            NPC(legend=random.randint(8, 10), debug=True))

    # for npc_type in encounter:
    #     [n.save_to_dict() for n in encounter[npc_type]]

    return encounter


class BattleEngine(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["create_encounter"])
    async def ce(self, ctx, encounter_id=0):
        if encounter_id > 0:
            encounter = get_encounter(encounter_id)
        else:
            encounter = random_encounter()

        encounter_group = []

        for npctype in encounter:
            for npc in encounter[npctype]:
                npc_player = npc.player
                clogger(npc_player)
                encounter_group.append(npc_player)

        player_list = ", ".join([p.display_name for p in ctx.message.mentions])
        player_ids = [p.id for p in ctx.message.mentions if p.is_bot is False]

        


        battle = Battle(participants)
        jb_results = battle.join_battle()

        group_size = len(participants)
        await ctx.send(f"```Starting encounter with {group_size}"
                       f"players: {player_list}], "
                       f"opponenets: {len(encounter_group)}.```")

        await ctx.send("```Rolling Join Battle```", delete_after=1.0)

        await ctx.send(f"```{jb_results}```")


def setup(client):
    client.add_cog(BattleEngine(client))
