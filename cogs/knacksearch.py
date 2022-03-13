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

from knacks import search_knacks

def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)

class KnackSearch(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot        
        
    @commands.command(aliases=["k","sk","knack","searchknack","searchknacks"])
    async def knacks(self, ctx):
        """Search knacks by full/partial name."""
        def chunks(lst):
            for i in range(0 , len(lst) , 7):
                yield lst[i:i + 7]

        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        await ctx.send(f"```Searching for knack containg the term: `{term}` ```", delete_after=5.0)
        title, description_list, tables = search_knacks(term)
        if title and description_list:
            embed = discord.Embed(title=f"{title}")
            description_message = []
            description_message = split_text(description_list)
            
            description_message_list = []
            embed.add_field(name="\u200b", value="\u200b", inline=True)
            
            for idx, dm in enumerate(description_message):
                if idx == 0:
                    embed.add_field(name="Rule as Written", value=f"```{dm}```", inline=False)
                else:
                    embed.add_field(name="\u200b", value=f"```{dm}```", inline=False)
            await ctx.send(embed=embed)

            if tables:
                for table in tables:
                    header = table["header"]
                    rows = table["rows"]
           
                    count = 0
                                    
                    for chunk in chunks(rows):
                        embed = discord.Embed()
                        embed.add_field(name=header[0], value=chunk[0][0])
                        embed.add_field(name=header[1], value=chunk[0][1])
                                
                        for i in range(1, 7):
                            embed.add_field(name="\u200b", value="\u200b") # adds a blank field to make it look nicer
                            embed.add_field(name="\u200b", value=chunk[i][0])
                            embed.add_field(name="\u200b", value=chunk[i][1])

                        count += 1
                        await ctx.send(embed=embed)
        else:
            await ctx.send(f"```\nNo knack found with term(s): `{term}` ```", delete_after=5.0)




def setup(client):
    client.add_cog(KnackSearch(client))