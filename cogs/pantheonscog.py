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

from pantheons import search_gods
from pantheons import search_pantheon
from pantheons import search_rivals
from pantheons import search_favoured

def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)

class Pantheonscog(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=["sf", "f", "searchfavoured"])
    async def favoured(self, ctx):
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        god_count = 0
        if term:
            favoured = search_favoured(term)
            for god in favoured:
                god_count += 1
                god_name = god["name"]
                # description = god["description"]
                pantheon = god["pantheon"]
                rivals = god["rivals"]
                favoured_epic_attributes = god["favoured"]["purviews"]
                favoured_abilities = god["favoured"]["epic_attributes"]
                favoured_purviews = god["favoured"]["abilities"]

                embed = discord.Embed()
                embed.add_field(name="God", value=god_name, inline=False)
                embed.add_field(name="Pantheon", value=pantheon, inline=False)
                embed.add_field(name="Rival Gods", value=", ".join(rivals), inline=False)
                embed.add_field(name="Favoured Aspects", value="\u200b", inline=False)
                embed.add_field(name="Attributes", value=", ".join(favoured_epic_attributes), inline=True)
                embed.add_field(name="Abilities", value=", ".join(favoured_abilities), inline=True)
                embed.add_field(name="Purviews", value=", ".join(favoured_purviews), inline=True)
                await ctx.send(embed=embed)
                # god_description=f"""```markdown\n{description}```"""
                # await ctx.send(god_description)

        await ctx.send(f"```markdwon\nSearch complete! Found {god_count} gods who have favoured aspects containing the term: `{term}`!")



    @commands.command(aliases=["r","sr","searchrivals","searchrival","lookuprivals","rivallookup","lookuprival"])
    async def rivals(self, ctx):
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        god_count = 0
        if term:
            rivals = search_rivals(term)
            for god in rivals:
                god_count += 1
                god_name = god["name"]
                # description = god["description"]
                pantheon = god["pantheon"]
                rivals = god["rivals"]
                favoured_epic_attributes = god["favoured"]["purviews"]
                favoured_abilities = god["favoured"]["epic_attributes"]
                favoured_purviews = god["favoured"]["abilities"]

                embed = discord.Embed()
                embed.add_field(name="God", value=god_name, inline=False)
                embed.add_field(name="Pantheon", value=pantheon, inline=False)
                embed.add_field(name="Rival Gods", value=", ".join(rivals), inline=False)
                embed.add_field(name="Favoured Aspects", value="\u200b", inline=False)
                embed.add_field(name="Attributes", value=", ".join(favoured_epic_attributes), inline=True)
                embed.add_field(name="Abilities", value=", ".join(favoured_abilities), inline=True)
                embed.add_field(name="Purviews", value=", ".join(favoured_purviews), inline=True)
                await ctx.send(embed=embed)
                # god_description=f"""```markdown\n{description}```"""
                # await ctx.send(god_description)
        await ctx.send(f"```markdown\nSearch complete! Found {god_count} rival god(s).```")

    @commands.command(aliases=["p","sp","searchpantheon","searchpantheons"])
    async def pantheons(self, ctx):
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        pantheon_count = 0
        god_count = 0
        if term:
            pantheons = search_pantheon(term)
            for pantheon in pantheons:
                pantheon_count += 1
                for god in pantheons[pantheon]:
                    god_count += 1
                    god_name = god["name"]
                    description = god["description"]
                    pantheon = god["pantheon"]
                    rivals = god["rivals"]
                    favoured_epic_attributes = god["favoured"]["purviews"]
                    favoured_abilities = god["favoured"]["epic_attributes"]
                    favoured_purviews = god["favoured"]["abilities"]

                    embed = discord.Embed()
                    embed.add_field(name="God", value=god_name)
                    embed.add_field(name="Pantheon", value=pantheon)
                    embed.add_field(name="Rival Gods", value=", ".join(rivals))
                    embed.add_field(name="Favoured Aspects", value="\u200b", inline=True)
                    embed.add_field(name="Attributes", value=", ".join(favoured_epic_attributes), inline=True)
                    embed.add_field(name="Abilities", value=", ".join(favoured_abilities), inline=True)
                    embed.add_field(name="Purviews", value=", ".join(favoured_purviews), inline=True)

                    await ctx.send(embed=embed)
                    # god_description=f"""```markdown\n{description}```"""
                    # await ctx.send(god_description)
        await ctx.send(f"```markdown\nSearch complete! Found {god_count} god(s) from {pantheon_count} pantheon(s).```")
        

    @commands.command(aliases=["g","sg","god","searchgod","searchgods"])
    async def gods(self, ctx):
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        if term:
            god = search_gods(term)
            if god:
                god_name = god["name"]
                description = god["description"]
                pantheon = god["pantheon"]
                rivals = god["rivals"]
                favoured_epic_attributes = god["favoured"]["purviews"]
                favoured_abilities = god["favoured"]["epic_attributes"]
                favoured_purviews = god["favoured"]["abilities"]

                embed = discord.Embed()
                embed.add_field(name="God", value=god_name)
                embed.add_field(name="Pantheon", value=pantheon)
                embed.add_field(name="Rival Gods", value=", ".join(rivals))
                embed.add_field(name="Favoured Aspects", value="\u200b", inline=True)
                embed.add_field(name="Attributes", value=", ".join(favoured_epic_attributes), inline=True)
                embed.add_field(name="Abilities", value=", ".join(favoured_abilities), inline=True)
                embed.add_field(name="Purviews", value=", ".join(favoured_purviews), inline=True)

                
                await ctx.send(embed=embed)
                god_description=f"""```markdown\n{description}```"""
                await ctx.send(god_description)            
                return

            await ctx.send(f"```markdown\nSearch complete! No gods containing `{term}` in their name were found!```")
            return
        await ctx.send("```markdown\nPlease enter the name or partial name of a god to search...```")


def setup(client):
    client.add_cog(Pantheonscog(client))