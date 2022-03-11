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


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)

class DiceLogs(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(aliases=["dl","dicelogs","dicehistory"])
    async def dicelog(self, ctx, limit: int = 20):
        dicelogger = ["```markdown","\n"]
        logs_list = []        

        with open("dicelogs.json", "r") as f:
            SESSION_RESULTS = json.load(f)

        if len(SESSION_RESULTS.keys()) > 0:
            for key in SESSION_RESULTS.keys():
                for log in SESSION_RESULTS[key]:
                    logs_list.append(log)

        await self.returnDiceLogs(ctx, logs_list, dicelogger, limit)

    async def returnDiceLogs(self, ctx, logs_list:list=[], dicelogger:list=[], limit:int =20):
            if len(logs_list) == 0:
                await ctx.send("```markdown\nThere are no dice logs yet.```")
                return
            else:
                
                if len(logs_list) < limit:
                    limit = len(logs_list) * -1
                else:
                    limit = limit * -1 

                for idx, log in enumerate(logs_list):
                    if(len(logs_list[idx]) == 1):
                        logs_list = logs_list[idx]

                    date = logs_list[idx][0]
                    name = logs_list[idx][1]
                    roll_string = logs_list[idx][2]
                    dice_results = logs_list[idx][3]
                    successes = logs_list[idx][4]
                    auto_succ = logs_list[idx][5]
                    total_succ = logs_list[idx][6]
                    logs_list[idx] = f"<{date}> [{name}]. Roll string: {roll_string}.\n# Results: [S: {successes}] [A: {auto_succ}] [T: {total_succ}] - Raw results: [{dice_results}]".split(",")

                dicelogger.append("\n".join([",".join(l) for l in logs_list[limit:]]))        
                dicelogger.append("```")

                await ctx.send("\n".join(dicelogger))    


def setup(client):
    client.add_cog(DiceLogs(client))