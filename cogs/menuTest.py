import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

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

with open("config.json", "r") as f:
    config = json.load(f)


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)


class MenuTest(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["menutest"])
    async def mt(self, ctx):
        msg = await ctx.send(
            "What do you want to do?",
            components=[
                [
                    Button(label="Attack!", custom_id="attack", style=1),
                    Button(label="Aim!", custom_id="aim", style=2),
                    Button(label="Jump!", custom_id="jump", style=3),
                    Button(label="Roll!", custom_id="roll", style=4),
                    Button(label="Rule check!", custom_id="url",
                           style=5, url="https://www.google.com")
                ],
                [
                    Select(
                        placeholder="Use a Knack or Boon!",
                        options=[
                            SelectOption(label="Select a Boon", value="boon"),
                            SelectOption(label="Select a Knack", value="knack")
                        ])
                ]
            ])

        interaction = await self.bot.wait_for("button_click", check=lambda i: i.custom_id in ["attack", "aim", "jump", "roll", "url"] and i.user.id == ctx.author.id)
        await interaction.send(content=f"You clicked: {interaction.custom_id}!", delete_after=5.0)
        await ctx.send(content=f"```{ctx.author.display_name} clicked an action!```")
        await msg.delete()


def setup(client):
    client.add_cog(MenuTest(client))
