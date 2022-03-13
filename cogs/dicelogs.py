import discord
from discord.ext import commands
from datetime import datetime
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
        """Show the dice logs for all users."""
        logs_list = []        

        with open("dicelogs.json", "r") as f:
            SESSION_RESULTS = json.load(f)

        if len(SESSION_RESULTS.keys()) > 0:
            for key in SESSION_RESULTS.keys():
                for log in SESSION_RESULTS[key]:
                    logs_list.append(log)

        await self.returnDiceLogs(ctx, None, logs_list, limit)

    @commands.command(aliases=["dlu","userdicelogs","rollhistory","userdicehistory","dicelogsuser"])
    async def diceloguser(self, ctx, member: discord.Member = None, limit: int = 20):
        """Show the dice logs for a given user."""
        logs_list = []
        
        with open("dicelogs.json", "r") as f:
            SESSION_RESULTS = json.load(f)

        target = discord.utils.get(self.bot.get_all_members(), id=member.id)

        if target:
            if str(target.id) in SESSION_RESULTS.keys(): 
                for log in SESSION_RESULTS[str(target.id)]:
                    logs_list.append(log)
                await self.returnDiceLogs(ctx, target, logs_list, limit)
                return
            else:
                await ctx.send(f"```There are no logs for {target.display_name}! {target.display_name} has not rolled any dice yet.```")
                return
        await ctx.send(f"```Please provide a target user.\nExample: ?[diceloguser|dlu] @someone [limit].```", delete_after=5.0)
        return


    async def returnDiceLogs(self, ctx, member:discord.Member = None, logs_list:list = [], limit:int = 10):
            if len(logs_list) == 0:
                await ctx.send("```There are no dice logs yet.```", delete_after=5.0)
                return
            else:
                
                if len(logs_list) < limit:
                    limit = len(logs_list)

                if limit >= 1:
                    limit *= -1
                
                embed = discord.Embed()
                if member:
                    embed.title = f"Logs for {member.display_name.title()}"
                #logs_list.reverse()
                limited_log_list = logs_list[limit - 1:-1]
                limited_log_list = sorted(limited_log_list, key=lambda x: datetime.strptime(x[0], '%d-%m-%Y @ %H:%M:%S:%f'))
                for idx, log in enumerate(limited_log_list):
                    if(len(logs_list[idx]) == 1):
                        logs_list = limited_log_list[idx]

                    date = limited_log_list[idx][0]
                    name = limited_log_list[idx][1]
                    roll_string = limited_log_list[idx][2]
                    dice_results = limited_log_list[idx][3]
                    successes = limited_log_list[idx][4]
                    auto_succ = limited_log_list[idx][5]
                    total_succ = limited_log_list[idx][6]
                    embed.add_field(name=f"{date} :: Raw command: {roll_string}", value=f"```markdown\n# [S: {successes}] [A: {auto_succ}] [T: {total_succ}]\nRaw results: {dice_results}```", inline=False)
                
                return await ctx.send(embed=embed)    


def setup(client):
    client.add_cog(DiceLogs(client))