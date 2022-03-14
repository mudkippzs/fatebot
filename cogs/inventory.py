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

with open("inventory.json", "r") as f:
        global_inventory = json.load(f)

with open("config.json", "r") as f:
    config = json.load(f)

def load_global_inventory():
    with open("inventory.json", "r") as f:
        gi = json.load(f)
    return gi

def save_global_inventory():
    with open("inventory.json", "w") as f:
        f.write(json.dumps(global_inventory))

def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)

def command_verb(command):
    command_verbs = {
        'add': ['adds to'],
        'remove': ['removes from'],
        'check': ['checks for'],
        'search': ['searches'],
        'random': ['pulls a random item from'],
    }
    return command_verbs[command][0]


def get_user_inventory(user):
    inv = ["```markdown\n"]
    if len(global_inventory[str(user)]):
        for item in global_inventory[str(user)]:
            i = item[0]
            q = item[1]
            d = item [2]

            inv.append(f"* {q} x {i} - {d}")
        inv.append("```")
    else:
        return f"```markdown\nNo items in inventory.```"
    return "\n".join(inv)

def add_to_user_inventory(user, item, quantity=1, description="Non-descript item."):
    if str(user) not in global_inventory.keys():
        global_inventory[str(user)] = []
    for idx, inv_item in enumerate(global_inventory[str(user)]):
            if inv_item[0].lower() == item.lower():
                global_inventory[str(user)][idx][1] += quantity
                if description:
                    if description.lower() != inv_item[2].lower():                    
                        global_inventory[str(user)][idx][2] = description.lower()
                    else:
                        global_inventory[str(user)][idx][2] = global_inventory[str(user)][idx][2]
                save_global_inventory()
                return get_user_inventory(user)
    global_inventory[str(user)].append([item, quantity, description])
    save_global_inventory()
    return get_user_inventory(user)

def remove_from_user_inventory(user, item, quantity):
    if str(user) in global_inventory.keys():
        for idx, inv_item in enumerate(global_inventory[str(user)]):
            if item.lower() == inv_item[0].lower():
                global_inventory[str(user)][idx][1] -= quantity
            if global_inventory[str(user)][idx][1] < 1:
                del global_inventory[str(user)][idx]

    save_global_inventory()
    return get_user_inventory(user)

def search_in_user_inventory(user, item):
    for inv_item in global_inventory[str(user)]:
        if item.lower() == inv_item[0].lower():
            return inv_item[0], inv_item[1], inv_item[2]        
    return 0,0,0

def get_random_item_from_inventory(user):
    if str(user) in global_inventory.keys():
        random_item = random.choice(global_inventory[str(user)])
        return random_item[0], random_item[1], random_item[2]
    else:
        return 0,0,0

class InventoryManager(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot
        load_global_inventory()    
        
    @commands.command(aliases=["ai", "ainv", "abag"])
    async def admininventory(self, ctx, user: discord.Member = None, command: str = "check", item: str = None, quantity: int = 1, description: str = "No description"):
        """Admin Inventory management - add, remove, check, search, draw a random item; from your inventory."""
        if str(ctx.message.author.id) not in [config["gamemaster"][0]["ganj"]]:
            await ctx.send("```Only Gamemasters can access other people's inventory. You are not a Gamemaster.```", delete_after=5.0)
            return

        if user is None:
            user = ctx.author

        global_inventory = load_global_inventory()

        if quantity < 1:
            quantity = 1

        if quantity > 1000000:
            quantity = 1000000
        
        if command not in ["add", "remove", "check", "search", "random"]:
            await ctx.send(f"```Unknown command. Please try again.\nUsage: ?inventory [add/remove/check/search/random] item[optional] quantity[optional] description[optional]```", delete_after=5.0)
            return
        
        if "add" in command:
            inventory = add_to_user_inventory(user.id, item, quantity, description)
            await ctx.send(f"```{ctx.message.author} {command_verb(command)} {user}'s inventory: `{item}` ```")
            await ctx.send(inventory)
            
        elif "remove" in command:
            inventory = remove_from_user_inventory(user.id, item, quantity)
            await ctx.send(f"```{ctx.message.author} {command_verb(command)} {user}'s inventory: {quantity} x `{item}` ```")
            await ctx.send(inventory)
            
        elif "check" in command:
            if str(ctx.message.author.id) in global_inventory.keys():
                await ctx.send(f"```{ctx.message.author} {command_verb(command)} {user}'s inventory...```")
                inventory = get_user_inventory(user.id)
                await ctx.send(inventory)
            else:
                await ctx.send(f"```{ctx.message.author} has no items in {user}'s inventory.```", delete_after=5.0)

        elif "search" in command:
            await ctx.send(f"```{ctx.message.author} {command_verb(command)} {user}'s inventory for `{item}`...```")
            search_item, search_item_quantity, search_item_description = search_in_user_inventory(user.id, item)
            if search_item == 0:
                await ctx.send(f"```{ctx.message.author} didn't find `{item}` in {user}'s inventory.```", delete_after=5.0)
                inventory = get_user_inventory(user.id)
                await ctx.send(inventory)
            else:
                await ctx.send(f"```{ctx.message.author} found:``` `{search_item} ({search_item_quantity}) - {search_item_description}`")
        
        elif "random" in command:
            await ctx.send(f"```{ctx.message.author} {command_verb(command)} {user}'s inventory...```")
            random_item, random_item_quantity, random_item_description = get_random_item_from_inventory(user.id)
            if random_item != 0:
                await ctx.send(f"```{ctx.message.author} pulled out:``` `{random_item} ({random_item_quantity}) - {random_item_description}`")
            else:
                await ctx.send(f"```{ctx.message.author} has no items in {user}'s inventory.```", delete_after=5.0)

        return
        
    @commands.command(aliases=["i", "inv", "bag"])
    async def inventory(self, ctx, command: str = "check", item: str = None, quantity: int = 1, description: str = "No description"):
        """Inventory management - add, remove, check, search, draw a random item; from your inventory."""
        global_inventory = load_global_inventory()

        if quantity < 1:
            quantity = 1

        if quantity > 1000000:
            quantity = 1000000
        
        if command not in ["add", "remove", "check", "search", "random"]:
            await ctx.send(f"```Unknown command. Please try again.\nUsage: ?inventory [add/remove/check/search/random] item[optional] quantity[optional] description[optional]```", delete_after=5.0)
            return
        
        if "add" in command:
            inventory = add_to_user_inventory(ctx.message.author.id, item, quantity, description)
            await ctx.send(f"```{ctx.message.author} {command_verb(command)} their inventory: `{item}` ```")
            await ctx.send(inventory)
        
        elif "remove" in command:
            inventory = remove_from_user_inventory(ctx.message.author.id, item, quantity)
            await ctx.send(f"```{ctx.message.author} {command_verb(command)} their inventory: {quantity} x `{item}` ```")
            await ctx.send(inventory)
        
        elif "check" in command:
            if str(ctx.message.author.id) in global_inventory.keys():
                await ctx.send(f"```{ctx.message.author} {command_verb(command)} their inventory...```")
                inventory = get_user_inventory(ctx.author.id)
                await ctx.send(inventory)
            else:
                await ctx.send(f"```{ctx.message.author} has no items in their inventory.```")

        elif "search" in command:
            await ctx.send(f"```{ctx.message.author} {command_verb(command)} their inventory for `{item}`...```")
            search_item, search_item_quantity, search_item_description = search_in_user_inventory(ctx.message.author.id, item)
            if search_item == 0:
                await ctx.send(f"```{ctx.message.author} didn't find `{item}` in their inventory.```")
                inventory = get_user_inventory(ctx.author.id)
                await ctx.send(inventory)
            else:
                await ctx.send(f"```{ctx.message.author} found: `{search_item} ({search_item_quantity})` - `{search_item_description}`")
        
        elif "random" in command:
            await ctx.send(f"```{ctx.message.author} {command_verb(command)} their inventory...```")
            random_item, random_item_quantity, random_item_description = get_random_item_from_inventory(ctx.message.author.id)
            if random_item != 0:
                await ctx.send(f"```{ctx.message.author} pulled out:``` `{random_item} ({random_item_quantity}) - {random_item_description}`")
            else:
                await ctx.send(f"```{ctx.message.author} has no items in their inventory.```")

        return


def setup(client):
    client.add_cog(InventoryManager(client))