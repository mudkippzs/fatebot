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

from cogs.character import Character


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


def random_encounter(context):

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
        encounter["civilians"].append(NPC(legend=0, context=context, debug=True))

    # for i in range(10):
    #     encounter["grunts"].append(
    #         NPC(label=f"Cultist of Ymir #{i}", legend=random.randint(1, 2), debug=True))

    # for _ in range(4):
    #     encounter["peons"].append(NPC(legend=random.randint(0, 1), debug=True))

    # for _ in range(3):
    #     encounter["miniboss"].append(
    #         NPC(legend=random.randint(3, 5), debug=True))

    # for _ in range(3):
    #     encounter["boss"].append(NPC(legend=random.randint(4, 6), debug=True))

    # for _ in range(3):
    #     encounter["bigboss"].append(
    #         NPC(legend=random.randint(6, 7), debug=True))

    # for _ in range(3):
    #     encounter["deadly"].append(
    #         NPC(legend=random.randint(8, 10), debug=True))

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
            encounter = random_encounter(ctx)

        encounter_group = []

        for npctype in encounter:
            for npc in encounter[npctype]:
                npc_player = npc.player
                encounter_group.append(npc_player)

        player_list = ", ".join([p.display_name for p in ctx.message.mentions])
        player_ids = [p for p in ctx.message.mentions]

        import_roster = Character.load_characters_from_files(None)
        player_count = 0
        for pc in import_roster:
            if pc["player_id"] in [p.id for p in player_ids]:
                player_count += 1
                encounter_group.append(Player(name=pc["name"],
                                              discord_tag=pc["player_id"],
                                              npc=False,
                                              legend=pc["legend"],
                                              options=pc))
   
        battle = Battle(encounter_group)

        group_size = len(encounter_group)
        await ctx.send(f"```Starting encounter with {player_count} "
                       f"players: {player_list}, and "
                       f"{len(encounter_group) - player_count} opponents.```")

        await ctx.send("```Rolling Join Battle```", delete_after=5.0)
        battle_engaged = True
        while battle_engaged:
            await battle.before_tick(ctx)
            await battle.do_tick(ctx, self.bot)
            await battle.after_tick(ctx)
            battle.next_tick()
            if battle.current_tick >= 21:
                battle_engaged = False


def setup(client):
    client.add_cog(BattleEngine(client))
