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

from pantheons import search_gods
from pantheons import search_pantheon
from pantheons import search_rivals
from pantheons import search_favoured


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)


def split_list(lst):
    """Split list into lists of length 10 or less."""

    new_list = []

    for i in range(0, len(lst), 10):
        new_list.append(lst[i:i + 10])

    return new_list


class PantheonSearch(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sf", "f", "searchfavoured", "fe", "fa", "fp"])
    async def favoured(self, ctx):
        """Find which gods favor a given epic attirbute(epic dexterity, epic perception etc.), purview (water, arete, chaos...etc.) or ability (athletics, science, survival...etc.)."""
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        god_count = 0
        if term:
            await ctx.send(f"```Searching for favoured aspects containing the term: `{term}`...```", delete_after=5.0)
            favoured = split_list(search_favoured(term))
            for fav_set in favoured:
                if god_count > 1:
                    embed = discord.Embed(
                        title=f"Gods with favoured aspects of \"{term.title()}\"")
                else:
                    embed = discord.Embed(title=f"\u200b")
                for god in fav_set:
                    god_count += 1
                    aka = ", ".join(god["aka"])
                    god_name = god["name"].title()
                    pantheon = god["pantheon"].title()
                    purviews = [p.title() for p in god["favoured"]["purviews"]]
                    epic_attributes = [p.title()
                                       for p in god["favoured"]["epic_attributes"]]
                    abilities = [p.title()
                                 for p in god["favoured"]["abilities"]]

                    god_text = (f"```Purivews: {', '.join(purviews)}\n\n"
                                f"Attributes: {', '.join(epic_attributes)}\n\n"
                                f"Abilities: {', '.join(abilities)}```")

                    embed.add_field(
                        name=f"{god_name} (AKA: {aka}) of the {pantheon}", value=god_text, inline=False)
                await ctx.send(embed=embed)

        await ctx.send(f"```Search complete! Found {god_count} rival god(s).```", delete_after=5.0)

    @commands.command(aliases=["r", "sr", "searchrivals", "searchrival", "lookuprivals", "rivallookup", "lookuprival"])
    async def rivals(self, ctx):
        """List the rival gods of a given god."""
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        god_count = 0
        if term:
            await ctx.send(f"```Searching for rivals of `{term}`...```", delete_after=5.0)
            rivals = search_rivals(term)
            if len(rivals):
                embed = discord.Embed(title=f"Rival Gods of {term.title()}")
                for god in rivals:
                    god_count += 1
                    aka = ", ".join(god["aka"])
                    god_name = god["name"].title()
                    pantheon = god["pantheon"].title()
                    purviews = [p.title() for p in god["favoured"]["purviews"]]

                    god_text = f"```God of ({', '.join(purviews)})```"

                    embed.add_field(
                        name=f"{god_name} (AKA: {aka}) of the {pantheon}", value=god_text, inline=False)
                await ctx.send(embed=embed)

        await ctx.send(f"```Search complete! Found {god_count} rival god(s).```", delete_after=5.0)

    @commands.command(aliases=["p", "sp", "searchpantheon", "searchpantheons"])
    async def pantheons(self, ctx):
        """List the Gods of a given Pantheon."""
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        pantheon_count = 0
        total_god_count = 0
        if term:
            pantheons = search_pantheon(term)
            for pantheon in pantheons:
                embed = discord.Embed(title=f"Gods of the {pantheon.title()}")
                pantheon_count += 1
                god_count = 0
                for god in pantheons[pantheon]:
                    god_count += 1
                    god_name = god["name"].title()
                    aka = ", ".join(god["aka"])
                    pantheon = god["pantheon"]
                    purviews = [p.title() for p in god["favoured"]["purviews"]]
                    epic_attributes = [p.title()
                                       for p in god["favoured"]["epic_attributes"]]
                    abilities = [p.title()
                                 for p in god["favoured"]["abilities"]]

                    god_text = (f"```Purivews: {', '.join(purviews)}\n\n"
                                f"Attributes: {', '.join(epic_attributes)}\n\n"
                                f"Abilities: {', '.join(abilities)}```")

                    embed.add_field(
                        name=f"{god_name} (AKA: {aka})", value=god_text, inline=False)

                await ctx.send(embed=embed)
                total_god_count += god_count
        await ctx.send(f"```Search complete! Found {god_count} god(s) from {pantheon_count} pantheon(s).```", delete_after=5.0)

    @commands.command(aliases=["g", "sg", "god", "searchgod", "searchgods"])
    async def gods(self, ctx):
        """Search for a God by name."""
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        if term:
            god = search_gods(term)
            if god:
                god_name = god["name"].title()
                aka = ", ".join(god["aka"])
                description_full = god["description"]
                description_split = description_full.split("\n\n")
                description_lists = split_list(description_split)
                description_split_parsed = []

                for l in description_split:
                    l_new = [ln for ln in l.split(".")]
                    description_split_parsed.append(l_new)

                pantheon = god["pantheon"]
                rivals = ", ".join(god["rivals"])
                purviews = [p.title() for p in god["favoured"]["purviews"]]
                epic_attributes = [p.title()
                                   for p in god["favoured"]["epic_attributes"]]
                abilities = [p.title() for p in god["favoured"]["abilities"]]

                god_text = (f"```Purivews: {', '.join(purviews)}\n\n"
                            f"Attributes: {', '.join(epic_attributes)}\n\n"
                            f"Abilities: {', '.join(abilities)}```")

                embed = discord.Embed(
                    title=f"{god_name} (AKA: {aka}) of the {pantheon}")

                embed.add_field(name=f"Purviews",
                                value=', '.join(purviews), inline=True)
                embed.add_field(name=f"Epic Attributes",
                                value=', '.join(epic_attributes), inline=True)
                embed.add_field(name=f"Abilities", value=', '.join(
                    abilities), inline=False)
                await ctx.send(embed=embed)

                embed_rivals = discord.Embed(title=f"Rivals of {god_name}")
                embed_rivals.add_field(
                    name=f"\u200b", value=f"```{rivals}```", inline=True)
                await ctx.send(embed=embed_rivals)

                for idx, d in enumerate(description_split_parsed):
                    d_string = ". ".join(d)
                    if len(d_string):
                        if idx == 2:
                            break
                        if idx == 0:
                            embed_desc = discord.Embed(
                                title=f"About {god_name}")
                        else:
                            embed_desc = discord.Embed(title=f"\u200b")
                        embed_desc.add_field(
                            name=f"\u200b", value=f"```{d_string}```", inline=True)
                        await ctx.send(embed=embed_desc)

                await ctx.send(f"```Search for god with name containing `{term}` complete!```", delete_after=5.0)
                return

            await ctx.send(f"```Search complete! No gods containing `{term}` in their name were found!```", delete_after=5.0)
            return
        await ctx.send("```Please enter the name or partial name of a god to search...```", delete_after=5.0)


def setup(client):
    client.add_cog(PantheonSearch(client))
