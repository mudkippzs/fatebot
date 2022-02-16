"""
1. Using discordpy create a bootstrapped bot.
2. When the command "order66" is given by user ID 218521566412013568: get a list of users who reacted to message id 918514312186839050 in channel id 820097765442191360.
3. Kick all members who only have the role id 305756022562095104 who didn't react to the message with id 918514312186839050.
"""

import discord
from discord.ext import commands
from discord.utils import get
from pprint import pprint as pp
from knacks import search_knacks
from pantheons import PANTHEONS
from pantheons import search_gods
from pantheons import search_pantheon
from pantheons import search_rivals
from pantheons import search_favoured

from boons import search_boons
from split_text import split_text

import asyncio
import datetime
import json
import random
import re

EPIC_RATIOS = {
"0": 0,
"1": 1,
"2": 2,
"3": 4,
"4": 7,
"5": 11,
"6": 16,
"7": 22,
"8": 29,
"9": 37,
"10": 46,
"11": 56,
"12": 67,
"13": 79,
"14": 92,
"15": 106,
"16": 121,
"17": 137,
"18": 154,
"19": 172,
"20": 191,
"21": 211,
"22": 232,
"23": 254,
"24": 277,
"25": 301,
"26": 326,
"27": 352,
"28": 379,
"29": 407,
"30": 436,
"31": 466,
"32": 497,
"33": 529,
"34": 562,
"35": 596,
"36": 631,
"37": 667,
"38": 704,
"39": 742,
"40": 781,
"41": 821,
"42": 862,
"43": 904,
"44": 947,
"45": 991,
"46": 1036,
}

SESSION_RESULTS = {}

with open("config.json", "r") as f:
    config = json.load(f)

intents = discord.Intents(messages=True, members=True, guilds=True)
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.command(aliases=["sf", "f", "searchfavoured"])
async def favoured(ctx):
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



@bot.command(aliases=["r","sr","searchrivals","searchrival","lookuprivals","rivallookup","lookuprival"])
async def rivals(ctx):
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

@bot.command(aliases=["p","sp","searchpantheon","searchpantheons"])
async def pantheons(ctx):
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
    

@bot.command(aliases=["g","sg","god","searchgod","searchgods"])
async def gods(ctx):
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


@bot.event
async def on_ready():
    print("FateBot Online!")

@bot.command(aliases=["b","sb","boon","searchboon","searchboons"])
async def boons(ctx):
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

@bot.command(aliases=["k","sk","knack","searchknack","searchknacks"])
async def knacks(ctx):
    term = " ".join(ctx.message.clean_content.split(" ")[1:])
    title, description_list, tables = search_knacks(term)
    if title and description_list:
        title_message = f"```markdown\n# {title}```"

        description_message = []
        for description in description_list:
            if description:
                description_message.append(split_text(description))
        description_message_list = []
        for dm in description_message:
            description_message_list.append(f"```markdown\n{dm}\n```")
        await ctx.send(title_message)
        for dml in description_message_list:
            await ctx.send(dml)

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
        message = f"```ascidoc\nNo knack found with term(s): [{term}]```"
        await ctx.send(message)


def rolldice(roll_string:str = None):
    """Rolls dice for the given attribute, ability and epic attribute."""    
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
    extra_successes = EPIC_RATIOS[str(epic)]
    success_total = successes + extra_successes

    return dice_results, successes, extra_successes, success_total

@bot.command(aliases=["diceroll","rolldice"])
async def roll(ctx, roll_string:str = None):
    roll_string = roll_string.split(",")

    try:
        roll_string = [int(rs) for rs in roll_string]
    except ValueError:
        await ctx.send(f"""```markdown\nCommand help: ?roll 1,2,3 (attribute, ability, epic attribute).```""")
        return

    for value in roll_string:
        if value > 46 or value < 0 or sum(roll_string) < 1:
            await ctx.send(f"""```markdown\nCommand help: ?roll 1,2,3 (attribute, ability, epic attribute).```""")
            return
    if len(roll_string) == 3 and [int(rs) for rs in roll_string]:
        dice_results, successes, extra_successes, success_total = rolldice(roll_string)
        
        total_dice = 0
        
        for i in roll_string[0:2]:
            total_dice += i
        
        # Print results to discord channel.
        dice_results_string = ",".join(sorted([str(dr) for dr in dice_results]))
        dice_results_plurarl_string = "s" if total_dice > 1 else ""
        
        await ctx.send(f"```markdown\n# {ctx.message.clean_content} - Raw Results: [{dice_results_string}] {successes} successes + {extra_successes} automatic successes``````markdown\n{ctx.message.author.display_name} rolled {total_dice}D10{dice_results_plurarl_string} and got <{success_total} successes>!```")
        await ctx.message.delete()

        # Log it
        now = datetime.datetime.now()
        logstamp = now.strftime("%d-%m-%Y @ %H:%M:%S:%f")
        roll_log_string = [f"{logstamp}",f"{ctx.message.author}", f"{ctx.message.clean_content}", f"[{dice_results_string}]", f"S: {successes}", f"AS: {extra_successes}", f"T: {success_total}"]
        
        
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
            
    await ctx.send(f"""```markdown\nCommand help: ?roll 1,2,3 (attribute, ability, epic attribute).```""")
    return

@bot.command(aliases=["da","diceanal"])
async def diceanalytics(ctx):

    DICE_DISTRIBUTION = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 0,
    }

    def strip(s):
        return str(s.replace("[","").replace("]",""))

    with open("dicelogs.json", "r") as f:
        SESSION_RESULTS = json.load(f)

    for user_log in SESSION_RESULTS:
        for log in SESSION_RESULTS[user_log]:
            diceroll = [int(strip(dr)) for dr in log[3].split(",")]
            for dr in diceroll:
                DICE_DISTRIBUTION[str(dr)] += 1
    embed = discord.Embed()
    
    DICE_DISTRIBUTION = sorted(DICE_DISTRIBUTION, key=lambda x: x[0])
    
    embed.add_field(name="Dice Analytics", value="\u200b", inline=False)
    embed.add_field(name="Dice", value="\u200b", inline=True)
    embed.add_field(name="Value", value="\u200b", inline=True)
    message = []
    for key, value in enumerate(DICE_DISTRIBUTION):
        message.append(f"""{key} .................. {value}""")
    message_string = "\n".join(message)    
    embed.add_field(name=f"{message_string}", value=f"\u200b", inline=False)
    await ctx.send(embed=embed)
    return

@bot.command(aliases=["dlu","userdicelogs","rollhistory","userdicehistory","dicelogsuser"])
async def diceloguser(ctx, member: discord.Member=None):
    dicelogger = ["```markdown","\n"]
    logs_list = []
    try:
        target = ctx.message.mentions[0]
    except:
        target = ctx.message.author

    with open("dicelogs.json", "r") as f:
        SESSION_RESULTS = json.load(f)

    if target:
        try:
            logs_list = SESSION_RESULTS[str(target.id)]
        except KeyError:
            await ctx.send(f"```markdown\nThere are no logs for {target}! {target} has not rolled any dice yet.```")
            return
    else:        
        if len(SESSION_RESULTS.keys()) > 0:
            for key in SESSION_RESULTS.keys():
                logs_list.append(SESSION_RESULTS[key])
    
    limit = len(logs_list)    
    await returnDiceLogs(ctx, logs_list, dicelogger, limit)

@bot.command(aliases=["dl","dicelogs","dicehistory"])
async def dicelog(ctx, limit: int = 20):
    dicelogger = ["```markdown","\n"]
    logs_list = []        

    with open("dicelogs.json", "r") as f:
        SESSION_RESULTS = json.load(f)

    if len(SESSION_RESULTS.keys()) > 0:
        for key in SESSION_RESULTS.keys():
            for log in SESSION_RESULTS[key]:
                logs_list.append(log)

    await returnDiceLogs(ctx, logs_list, dicelogger, limit)

async def returnDiceLogs(ctx, logs_list:list=[], dicelogger:list=[], limit:int =20):
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

@bot.command(alias=["shieldsmokes"])
async def shieldsmoke(ctx):
    cigarette_brands = config["brands"].split(",")
    
    if ctx.message.author.id not in [218521566412013568, 514859386116767765]:
        await ctx.send("You are not Vasily, only Vasily can smoke Vasily's smokes...")
    else:
        if ctx.message.author.id == 514859386116767765:
            vasily = "Vasily opens his"
        else:
            vasily = f"{ctx.message.author.display_name} opens Vasily's"
        
        if ctx.message.mentions: 
            target = ctx.message.mentions[0].display_name
            await ctx.send(f"{vasily} divine cigarette case and pulls a **{random.choice(cigarette_brands)}** and passes it to {target}")
        else:            
            await ctx.send(f"{vasily} divine cigarette case and pulls a **{random.choice(cigarette_brands)}**")

@bot.command(name="purge")
async def purge(ctx, limit: int, member: discord.Member = None):
    if member is None:
        await ctx.channel.purge(limit=limit)
    else:
        await ctx.channel.purge(limit=limit, check=lambda m: m.author == member)



if __name__ == "__main__":
    bot.run(config["token"])
