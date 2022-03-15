import discord
from discord.ext import commands
import datetime
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
from epiccalc import calculate_epic


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)


def rolldice(roll_string: str = None):
    """Rolls dice for the given attribute, ability and epic attribute."""
    if type(roll_string) == str:
        roll_string = roll_string.split(",")
    attr = int(roll_string[0])
    ability = int(roll_string[1])
    epic = int(roll_string[2])

    # Calculate the number of dice to roll based on attr and ability.
    dice_to_roll = attr + ability

    # Roll the dice.
    dice_results = []
    for i in range(dice_to_roll):
        r = random.randint(1, 10)
        dice_results.append(r)

    # Count successes.
    successes = 0
    for i in range(len(dice_results)):
        if dice_results[i] >= 7:
            successes += 1
            if dice_results[i] > 9:
                successes += 1

    # Add extra successes based on epic attribute.
    extra_successes = calculate_epic(epic)
    success_total = successes + extra_successes

    return dice_results, successes, extra_successes, success_total


class Roller(commands.Cog):
    """Cog"""

    storyteller = None

    def __init__(self, bot):
        self.bot = bot
        self.storyteller = discord.utils.get(
            self.bot.get_all_members(), id=218521566412013568)
        # self.storyteller = False # To disable GM DMs for rolls.

    @commands.Cog.listener()
    async def on_ready(self):
        self.storyteller = discord.utils.get(
            self.bot.get_all_members(), id=218521566412013568)

    @commands.command(aliases=["ro", "dr", "diceroll", "rolldice"])
    async def roll(self, ctx, roll_string: str = None, privacy: bool = False, storyteller: discord.Member = False):
        """Roll a dice in Story Teller system. Fromat: Attr, Abil, Epic Attr. Example: ?roll 3,2,1"""
        roll_string = roll_string.split(",")
        if storyteller is False:
            self.storyteller = discord.utils.get(
                self.bot.get_all_members(), id=218521566412013568)

        try:
            roll_string = [int(rs) for rs in roll_string]
        except ValueError:
            await ctx.send(f"""```Command help: ?roll 1,2,3 (attribute, ability, epic attribute).```""", delete_after=5.0)
            return

        for value in roll_string:
            if value > 46 or value < 0 or sum(roll_string) < 1:
                await ctx.send(f"""```Command help: ?roll 1,2,3 (attribute, ability, epic attribute).```""", delete_after=5.0)
                return
        if len(roll_string) == 3 and [int(rs) for rs in roll_string]:
            dice_results, successes, extra_successes, success_total = rolldice(
                roll_string)

            total_dice = 0

            for i in roll_string[0:2]:
                total_dice += i

            # Print results to discord channel.
            dice_results_string = ",".join(
                sorted([str(dr) for dr in dice_results]))
            dice_results_plurarl_string = "s" if total_dice > 1 else ""
            clogger(
                f"{ctx.message.author.display_name} > {ctx.message.clean_content} <{success_total} successes> Raw Results: [{dice_results_string}] {successes} successes + {extra_successes} automatic successes")
            if privacy:
                await ctx.author.send(f"```markdown\n# {ctx.message.clean_content} - Raw Results: [{dice_results_string}] {successes} successes + {extra_successes} automatic successes``````markdown\n{ctx.message.author.display_name} rolled {total_dice}D10{dice_results_plurarl_string} and got < {success_total} successes >!```")

                with open("config.json", "r") as f:
                    config = json.load(f)
                #config["dm_snooze"] = False
                if config["dm_snooze"] == False:
                    await storyteller.send(f"```markdown\n# {ctx.message.clean_content} - Raw Results: [{dice_results_string}] {successes} successes + {extra_successes} automatic successes``````markdown\n{ctx.message.author.display_name} rolled {total_dice}D10{dice_results_plurarl_string} and got < {success_total} successes >!```")
                else:
                    await ctx.send(f"```No DM sent to Gamemaster - DM Snooze is enabled zZ!```", delete_after=5.0)
            else:
                await ctx.send(f"```markdown\n# {ctx.message.clean_content} - Raw Results: [{dice_results_string}] {successes} successes + {extra_successes} automatic successes``````markdown\n{ctx.message.author.display_name} rolled {total_dice}D10{dice_results_plurarl_string} and got < {success_total} successes >!```")

            # Log it
            now = datetime.datetime.now()
            logstamp = now.strftime("%d-%m-%Y @ %H:%M:%S:%f")
            roll_log_string = [f"{logstamp}", f"{ctx.message.author}", f"{ctx.message.clean_content}",
                               f"[{dice_results_string}]", f"{successes}", f"{extra_successes}", f"{success_total}"]

            with open("dicelogs.json", "r") as f:
                SESSION_RESULTS = json.load(f)

            try:
                if SESSION_RESULTS[str(ctx.author.id)]:
                    SESSION_RESULTS[str(ctx.author.id)].append(roll_log_string)
            except KeyError:
                SESSION_RESULTS[str(ctx.author.id)] = []
                SESSION_RESULTS[str(ctx.author.id)].append(roll_log_string)

            with open("dicelogs.json", "w+") as f:
                f.write(json.dumps(SESSION_RESULTS))

            return

        await ctx.send(f"""```Command help: ?roll 1,2,3 (attribute, ability, epic attribute).```""", delete_after=5.0)
        return success_total


def setup(client):
    client.add_cog(Roller(client))
