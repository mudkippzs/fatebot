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

from boons import search_boons

def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)

class Boonscog(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=["b","sb","boon","searchboon","searchboons"])
    async def boons(self, ctx):
        term = " ".join(ctx.message.clean_content.split(" ")[1:])
        boon_results = search_boons(term)
        if boon_results:
            for result in boon_results:
                title = result[0]
                description = result[1]
                message = f"""```markdown
{title}

{description}
```
"""
                await ctx.send(message)
        else:
            message = f"```ascidoc\nNo boon found with term(s): [{term}]```"
            await ctx.send(message)

    def chunks(lst):
        for i in range(0 , len(lst) , 7):
            yield lst[i:i + 7]


def setup(client):
    client.add_cog(Boonscog(client))