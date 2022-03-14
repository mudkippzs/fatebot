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

from boons import search_boons


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)


def get_boon_cost(description_text):
    if description_text.startswith("Cost"):
        description_text_split = description_text.split("\n")
        cost_text = description_text_split[0]
        dice_text = "\u200b"
        return cost_text, dice_text, description_text_split[1:][0]
    elif description_text.startswith("Dice"):
        description_text_split = description_text.split("\n")
        dice_text = "\n" + description_text_split[0]
        cost_text = description_text_split[1]
        return cost_text, dice_text, description_text_split[2:][0]
    return "\u200b"


class BoonSearch(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["b", "sb", "boon", "searchboon", "searchboons"])
    async def boons(self, ctx):
        """Search Boons by full/partial name."""
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        await ctx.send(f"```Searching for a boon containg the term: `{term}` ```")
        boon_results = search_boons(term)
        boon_count = 0
        if boon_results:
            for result in boon_results:
                boon_count += 1
                title = result[0]
                cost, dice_pool, description = get_boon_cost(result[1])

                embed = discord.Embed(title=title)
                embed_value = f"```{description}```"
                embed.add_field(name=f"{cost}{dice_pool}",
                                value=embed_value, inline=True)
                await ctx.send(embed=embed)
            await ctx.send(f"```Finished search, {boon_count} boons found containing the term: `{term}` ```")
        else:
            await ctx.send(f"```No boon found with term(s): {term}```", delete_after=5.0)

    def chunks(lst):
        for i in range(0, len(lst), 7):
            yield lst[i:i + 7]


def setup(client):
    client.add_cog(BoonSearch(client))
