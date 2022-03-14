import datetime
from difflib import SequenceMatcher

import discord
from discord.ext import commands
import glob
import importlib
import json
import os
import random
import re
import sys

from roller import Roller

import characters

from typing import List, Dict, Union, Optional
from epiccalc import calculate_epic

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger
from split_text import split_text

import atexit

with open("config.json", "r") as f:
    config = json.load(f)

with open("inventory.json", "r") as f:
    global_inventory = json.load(f)


def load_global_inventory():
    with open("inventory.json", "r") as f:
        gi = json.load(f)
    return gi


def save_global_inventory(gi):
    with open("inventory.json", "w") as f:
        f.write(json.dumps(gi))


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)


def attr_string_map(attribute):
    d = {
        "stre": "Strength",
        "dex": "Dexterity",
        "sta": "Statmina",
        "cha": "Charisma",
        "man": "Manipulation",
        "app": "Appearance",
        "per": "Perception",
        "inte": "Intelligence",
        "wits": "Wits"
    }
    return d[attribute]


def attr_to_dots(value=1, epic=False, ability=False):
    wc = "\u25CB"  # white circle
    bc = "\u25CF"  # black cirlce
    ws = "\u25A1"  # white square
    bs = "\u25A0"  # black square
    wstar = "\u2606"  # white star
    bstar = "\u2605"  # black star
    cstar = wstar
    if value > 10 and epic:
        cstar = bstar
        value -= 1

    if ability:
        attr_row = f"".rjust(value, bc) + (wc * (5 - value))
    elif epic:
        # 11th epic level is god-tier 'star'
        attr_row = f"".rjust(value, bs) + (ws * (10 - value)) + cstar
    else:
        attr_row = f"".rjust(value, bc) + (wc * (10 - value))
    return attr_row


def yards_to_kph(yards):
    return round((yards * 3.292), 2)


def yards_to_mph(yards):
    return round((yards * 2.045), 2)


def yards_to_mps(yards):
    return round((yards / 1.094), 2)


def yards_to_meters(yards):
    return round(yards / 1.094, 2)


def sort_abilities_list(ability_list_unsorted: list):
    """Transpose the ability list so that it appears in discord embed in a mirror format of the character sheet."""
    ability_list_sorted = {
        "academics": ability_list_unsorted["academics"],
        "craft": ability_list_unsorted["craft"],
        "melee": ability_list_unsorted["melee"],
        "animal_ken": ability_list_unsorted["animal_ken"],
        "empathy": ability_list_unsorted["empathy"],
        "occult": ability_list_unsorted["occult"],
        "art": ability_list_unsorted["art"],
        "politics": ability_list_unsorted["politics"],
        "athletics": ability_list_unsorted["athletics"],
        "fortitude": ability_list_unsorted["fortitude"],
        "presence": ability_list_unsorted["presence"],
        "awareness": ability_list_unsorted["awareness"],
        "integrity": ability_list_unsorted["integrity"],
        "science": ability_list_unsorted["science"],
        "brawl": ability_list_unsorted["brawl"],
        "investigation": ability_list_unsorted["investigation"],
        "command": ability_list_unsorted["command"],
        "stealth": ability_list_unsorted["stealth"],
        "larceny": ability_list_unsorted["larceny"],
        "control": ability_list_unsorted["control"],
        "marksmanship": ability_list_unsorted["marksmanship"],
        "survival": ability_list_unsorted["survival"],
        "medicine": ability_list_unsorted["medicine"],
        "thrown": ability_list_unsorted["thrown"],
    }

    return ability_list_sorted


def sort_attr_list(attr_list_unsorted: list, epic=False):
    """Transpose the attribute list so that it appears in discord embed in a mirror format of the character sheet."""

    if epic:
        attr_list_sorted = {
            "epic_stre": attr_list_unsorted["epic_stre"],  # STR
            "epic_cha": attr_list_unsorted["epic_cha"],  # CHA
            "epic_per": attr_list_unsorted["epic_per"],  # PER
            "epic_dex": attr_list_unsorted["epic_dex"],  # DEX
            "epic_man": attr_list_unsorted["epic_man"],  # MAN
            "epic_inte": attr_list_unsorted["epic_inte"],  # INT
            "epic_sta": attr_list_unsorted["epic_sta"],  # STA
            "epic_app": attr_list_unsorted["epic_app"],  # APP
            "epic_wits": attr_list_unsorted["epic_wits"],  # WIT
        }
    else:
        attr_list_sorted = {
            "stre": attr_list_unsorted["stre"],  # STR
            "cha": attr_list_unsorted["cha"],  # CHA
            "per": attr_list_unsorted["per"],  # PER
            "dex": attr_list_unsorted["dex"],  # DEX
            "man": attr_list_unsorted["man"],  # MAN
            "inte": attr_list_unsorted["inte"],  # INT
            "sta": attr_list_unsorted["sta"],  # STA
            "app": attr_list_unsorted["app"],  # APP
            "wits": attr_list_unsorted["wits"],  # WIT
        }
    return attr_list_sorted


class Character(commands.Cog):
    """Character Sheets"""

    def __init__(self, bot):
        self.bot = bot
        self.character_roster = []
        character_dir = characters.__path__[0]
        self.storyteller = discord.utils.get(
            self.bot.get_all_members(), id=218521566412013568)
        for root, dirs, files in os.walk(character_dir):  # pylint: disable=unused-variable
            for file in files:
                # only python script is allowed to be imported.
                if file.startswith("pc_") and file.endswith(".py"):
                    player_file = os.path.join(root, file)
                    # remove ".py" from the end of the filename
                    module_name = os.path.basename(player_file)[:-3]
                    spec = importlib.util.spec_from_file_location(
                        module_name, player_file)  # pylint: disable=no-member
                    module = importlib.util.module_from_spec(
                        spec)  # pylint: disable=no-member
                    spec.loader.exec_module(
                        module)  # pylint: disable=no-member
                    self.character_roster.append(module.PLAYER_CHARACTER_SHEET)

        self.recalculate_player_sheet()

    @commands.Cog.listener()
    async def on_ready(self):
        self.storyteller = discord.utils.get(
            self.bot.get_all_members(), id=218521566412013568)
        await self.initial_load_characters()
        self.recalculate_player_sheet()
        atexit.register(self.__save_characters)

    @commands.command()
    async def dc(self, ctx=None):
        if str(ctx.author.id) not in [config["gamemaster"][0]["ganj"]]:
            await ctx.send("```Only the GM can dump the character cache.```", delete_after=5.0)
            return
        for character in self.character_roster:
            clogger(character["inventory"])

    def sync_inventories(self):
        global_inventory = load_global_inventory()
        for idx, character in enumerate(self.character_roster):
            pid = character["player_id"]
            try:
                player_global_inventory = global_inventory[str(pid)]
            except KeyError as e:
                clogger(f"No bag found for {character['name']} ({pid})")
                global_inventory[str(pid)] = [[]]
                player_global_inventory = global_inventory[str(pid)]

            character["inventory"] = player_global_inventory
            self.character_roster[idx]["inventory"] = character["inventory"]
        save_global_inventory(global_inventory)
        return

    @commands.command()
    async def si(self, ctx=None):
        if str(ctx.author.id) not in [config["gamemaster"][0]["ganj"]]:
            await ctx.send("```Only the GM can sync inventories.```", delete_after=5.0)
            return

        self.sync_inventories()
        return

    @commands.command()
    async def load_characters(self, ctx=None):
        directory = "characters/exports/"
        player_ids = [pid for _, pid in config["players"][0].items()]
        most_recent_characters_exports = [k for k in sorted(os.listdir(directory), key=lambda f: os.path.getmtime(
            os.path.join(directory, f)), reverse=True) if k.endswith(".py") == False][0:len(player_ids)]
        import_roster = []

        for filename in most_recent_characters_exports:
            for pid in player_ids:
                if pid in filename[0:20]:
                    with open(os.path.join(directory, filename)) as f:
                        import_roster.append(json.load(f))

        for import_character in import_roster:
            for idx, character in enumerate(self.character_roster):
                if character["player_id"] == import_character["player_id"]:
                    self.character_roster[idx] = import_character

        clogger("Import finished.")
        self.recalculate_player_sheet()

        return None

    async def initial_load_characters(self):
        directory = "characters/exports/"
        player_ids = [pid for _, pid in config["players"][0].items()]
        most_recent_characters_exports = [k for k in sorted(os.listdir(directory), key=lambda f: os.path.getmtime(
            os.path.join(directory, f)), reverse=True) if k.endswith(".py") == False][0:len(player_ids)]
        import_roster = []

        for filename in most_recent_characters_exports:
            for pid in player_ids:
                if pid in filename[0:20]:
                    with open(os.path.join(directory, filename)) as f:
                        import_roster.append(json.load(f))

        for import_character in import_roster:
            for idx, character in enumerate(self.character_roster):
                if character["player_id"] == import_character["player_id"]:
                    self.character_roster[idx] = import_character

        clogger("Import finished.")
        self.sync_inventories()
        self.refill_player_sheet_charges(initial=True)
        self.recalculate_player_sheet(initial=True)

        return None

    def __save_characters(self):
        for idx, character in enumerate(self.character_roster):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%z")
            with open(f"characters/exports/{character['player_id']}_{timestamp}_export.json", "w") as f:
                json.dump(self.character_roster[idx], f, indent=4)

    @commands.command()
    async def save_characters(self, ctx=None):
        if str(ctx.author.id) not in [config["gamemaster"][0]["ganj"]]:
            await ctx.send("```Only the GM can save characters.```", delete_after=5.0)
            return
        self.__save_characters()

    def refill_player_sheet_charges(self, target: discord.Member = None, initial=False):
        def recharge(sheet):
            # Legend & Willpower
            sheet["legend_points_total"] = sheet["legend"] * sheet["legend"]
            sheet["legend_points_current"] = sheet["legend_points_total"]

            sorted_virtues = sorted(sheet["virtues"])
            sheet["willpower_total"] = sorted_virtues[2] + sorted_virtues[3]
            sheet["willpower_current"] = sheet["willpower_total"]

            return sheet

        if target:
            player_sheet = [(idx, pc) for idx, pc in enumerate(
                self.character_roster) if pc["player_id"] == target.id][0]
            self.character_roster[player_sheet[0]] = recharge(player_sheet[1])
        else:
            for idx, pc in enumerate(self.character_roster):
                self.character_roster[idx] = recharge(pc)

        return

    def recalculate_player_sheet(self, initial=False):

        for idx, pc in enumerate(self.character_roster):
            player_sheet = pc

            # Soaks & @TODO: Armor

            player_sheet["soak"]["bludgeon"] = player_sheet["attributes"]["sta"] + \
                calculate_epic(player_sheet["epic_attributes"]["epic_sta"])
            player_sheet["soak"]["lethal"] = round(
                player_sheet["soak"]["bludgeon"] / 2)
            player_sheet["soak"]["aggrevated"] = round(
                player_sheet["epic_attributes"]["epic_sta"] / 2)

            # Combat
            player_sheet["combat"]["dodge"][0] = (player_sheet["attributes"]["dex"] + player_sheet["abilities"]
                                                  ["athletics"] + player_sheet["legend"]) + calculate_epic(player_sheet["epic_attributes"]["epic_dex"]) / 2
            pc_brawl = player_sheet["abilities"]["brawl"]
            pc_melee = player_sheet["abilities"]["melee"]

            if pc_melee >= pc_brawl:
                player_sheet["combat"]["parry"][0] = (
                    player_sheet["attributes"]["dex"] + pc_melee) + calculate_epic(player_sheet["epic_attributes"]["epic_dex"]) / 2
            else:
                player_sheet["combat"]["parry"][0] = (
                    player_sheet["attributes"]["dex"] + pc_brawl) + calculate_epic(player_sheet["epic_attributes"]["epic_dex"]) / 2

            player_sheet["join_battle"] = player_sheet["attributes"]["wits"] + \
                player_sheet["abilities"]["awareness"] + \
                calculate_epic(player_sheet["epic_attributes"]["epic_wits"])

            # Movement
            player_sheet["movement"]["move"] = player_sheet["attributes"]["dex"] + \
                calculate_epic(player_sheet["epic_attributes"]["epic_dex"])
            player_sheet["movement"]["dash"] = player_sheet["movement"]["move"] + 6
            player_sheet["movement"]["climb"] = player_sheet["movement"]["move"] / 2
            player_sheet["movement"]["swim"] = player_sheet["movement"]["move"] / 2
            player_sheet["movement"]["jump"]["vertical"] = player_sheet["attributes"]["stre"] + calculate_epic(
                player_sheet["epic_attributes"]["epic_stre"]) + player_sheet["abilities"]["athletics"]
            player_sheet["movement"]["jump"]["horizontal"] = player_sheet["movement"]["jump"]["vertical"] * 2

            self.character_roster[idx] = player_sheet

        return

    @commands.command()
    async def ra(self, ctx):
        """Recalculate derived values and recharge legend and willpower."""
        if str(ctx.author.id) not in [config["gamemaster"][0]["ganj"]]:
            await ctx.send("```Only the GM can regen all characters.```", delete_after=5.0)
            return
        self.refill_player_sheet_charges()
        self.recalculate_player_sheet()

    @commands.command(aliases=["sheet", "charstats", "charsheet", "statsheet"])
    async def char(self, ctx, private=True, target: discord.Member = None, chained=False):
        await self.stats(ctx, private, target, True)
        await self.abilities(ctx, private, target, True)
        await self.movement(ctx, private, target, True)
        await self.combat(ctx, private, target, True)
        await self.myboons(ctx, private, target, True)
        await self.myknacks(ctx, private, target, True)

    @commands.command(aliases=["cat", "charattr"])
    async def stats(self, ctx, private=True, target: discord.Member = None, chained=False):
        if str(ctx.author.id) in [config["gamemaster"][0]["ganj"]] and target:
            player_key = target.id
        else:
            player_key = ctx.author.id
            if target:
                await ctx.send("```Only the GM can access other players character sheets.```", delete_after=5.0)

        player_sheet = [
            pc for pc in self.character_roster if pc["player_id"] == player_key]
        player_sheet = player_sheet[0]
        if chained == False:
            embed = discord.Embed(
                title=f"Attributes :: {player_sheet['name']} ```Player: {ctx.author.display_name}```")
        else:
            embed = discord.Embed(
                title=f"Character Sheet :: {player_sheet['name']} ```Player: {ctx.author.display_name}```")

        sorted_attributes = sort_attr_list(player_sheet["attributes"], False)
        sorted_epic_attributes = sort_attr_list(
            player_sheet["epic_attributes"], True)
        for attribute in sorted_attributes:
            attr_list = []
            attr_list.append(attr_to_dots(
                sorted_attributes[attribute], False))  # Standard Attrs
            attr_list.append(attr_to_dots(
                sorted_epic_attributes[f"epic_{attribute}"], True))  # Epic Attrs
            attr_string = "\n".join(attr_list)
            embed.add_field(name=attr_string_map(attribute), value=attr_string)

        if ctx.author == self.storyteller and private == True:
            await self.storyteller.send(embed=embed)
        elif private:
            await ctx.author.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=["cb"])
    async def myboons(self, ctx, private=True, target: discord.Member = None, chained=False):
        if str(ctx.author.id) in [config["gamemaster"][0]["ganj"]] and target:
            player_key = target.id
        else:
            player_key = ctx.author.id
            if target:
                await ctx.send("```Only the GM can access other players character sheets.```", delete_after=5.0)
        player_sheet = [
            pc for pc in self.character_roster if pc["player_id"] == player_key]
        player_sheet = player_sheet[0]
        embed = discord.Embed()
        if chained == False:
            embed.title = f"Boons :: {player_sheet['name']} ```Player: {ctx.author.display_name}```"

        boon_list = player_sheet["boons"]

        embed.add_field(
            name="\u200b", value=f"```{', '.join(boon_list)}```", inline=True)

        if ctx.author == self.storyteller and private == True:
            await self.storyteller.send(embed=embed)
        elif private:
            await ctx.author.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=["ck"])
    async def myknacks(self, ctx, private=True, target: discord.Member = None, chained=False):
        if str(ctx.author.id) in [config["gamemaster"][0]["ganj"]] and target:
            player_key = target.id
        else:
            player_key = ctx.author.id
            if target:
                await ctx.send("```Only the GM can access other players character sheets.```", delete_after=5.0)
        player_sheet = [
            pc for pc in self.character_roster if pc["player_id"] == player_key]
        player_sheet = player_sheet[0]
        embed = discord.Embed()
        if chained == False:
            embed.title = f"Knacks :: {player_sheet['name']} ```Player: {ctx.author.display_name}```"

        knack_list = player_sheet["knacks"]

        embed.add_field(
            name="\u200b", value=f"```{', '.join(knack_list)}```", inline=True)

        if ctx.author == self.storyteller and private == True:
            await self.storyteller.send(embed=embed)
        elif private:
            await ctx.author.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=["cab", "charabil"])
    async def abilities(self, ctx, private=True, target: discord.Member = None, chained=False):
        if str(ctx.author.id) in [config["gamemaster"][0]["ganj"]] and target:
            player_key = target.id
        else:
            player_key = ctx.author.id
            if target:
                await ctx.send("```Only the GM can access other players character sheets.```", delete_after=5.0)
        player_sheet = [
            pc for pc in self.character_roster if pc["player_id"] == player_key]
        player_sheet = player_sheet[0]
        embed = discord.Embed()
        if chained == False:
            embed.title = f"Abilities :: {player_sheet['name']} ```Player: {ctx.author.display_name}```"

        #sorted_abilities = sort_abilities_list(player_sheet["abilities"])
        sorted_abilities = player_sheet["abilities"]

        for ability in sorted_abilities:
            ability_list = []
            ability_list.append(attr_to_dots(
                sorted_abilities[ability], False, True))  # Standard Attrs
            ability_str = "\n".join(ability_list)
            embed.add_field(name=ability.title(),
                            value=ability_str, inline=True)

        if ctx.author == self.storyteller and private == True:
            await self.storyteller.send(embed=embed)
        elif private:
            await ctx.author.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=["co", "comb", "combsat"])
    async def combat(self, ctx, private=True, target: discord.Member = None, chained=False):
        if str(ctx.author.id) in [config["gamemaster"][0]["ganj"]] and target:
            player_key = target.id
        else:
            player_key = ctx.author.id
            if target:
                await ctx.send("```Only the GM can access other players character sheets.```", delete_after=5.0)

        player_sheet = [
            pc for pc in self.character_roster if pc["player_id"] == player_key]
        player_sheet = player_sheet[0]
        embed = discord.Embed()
        soak_b = player_sheet["soak"]["bludgeon"]
        soak_l = player_sheet["soak"]["lethal"]
        soak_a = player_sheet["soak"]["aggrevated"]

        armor_b = player_sheet["armor"]["bludgeon"]
        armor_l = player_sheet["armor"]["lethal"]
        armor_a = player_sheet["armor"]["aggrevated"]

        dodge_dv = player_sheet["combat"]["dodge"][0]
        parry_dv = player_sheet["combat"]["parry"][0]
        join_battle = player_sheet["attributes"]["wits"] + \
            player_sheet["abilities"]["awareness"]

        embed = discord.Embed(title="")
        if chained == False:
            embed.title = f"Combat Stats :: {player_sheet['name']} ```Player: {ctx.author.display_name}```"

        embed.add_field(
            name="\u200b", value=f"**Dodge DV**  `{dodge_dv:^5}`", inline=True)
        embed.add_field(
            name="\u200b", value=f"**Parry DV**  `{parry_dv:^5}`", inline=True)
        embed.add_field(
            name="\u200b", value=f"**Join Battle**  `{join_battle:^5}`", inline=True)
        embed.add_field(name="\u200b", value="**Soak**", inline=False)
        embed.add_field(
            name="\u200b", value=f"**Bludgeon**  `{soak_b:^5}`", inline=True)
        embed.add_field(
            name="\u200b", value=f"**Lethal**  `{soak_l:^5}`", inline=True)
        embed.add_field(
            name="\u200b", value=f"**Aggrevated**  `{soak_a:^5}`", inline=True)
        embed.add_field(name="\u200b", value="**Armor**", inline=False)
        embed.add_field(
            name="\u200b", value=f"**Bludgeon**  `{armor_b:^5}`", inline=True)
        embed.add_field(
            name="\u200b", value=f"**Lethal**  `{armor_l:^5}`", inline=True)
        embed.add_field(
            name="\u200b", value=f"**Aggrevated**  `{armor_a:^5}`", inline=True)

        if ctx.author == self.storyteller and private == True:
            await self.storyteller.send(embed=embed)
        elif private:
            await ctx.author.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=["mo", "mov", "movestat", "movestats"])
    async def movement(self, ctx, private=True, target: discord.Member = None, chained=False):
        if str(ctx.author.id) in [config["gamemaster"][0]["ganj"]] and target:
            player_key = target.id
        else:
            player_key = ctx.author.id
            if target:
                await ctx.send("```Only the GM can access other players character sheets.```", delete_after=5.0)

        player_sheet = [
            pc for pc in self.character_roster if pc["player_id"] == player_key]
        player_sheet = player_sheet[0]
        embed = discord.Embed()
        move = player_sheet["movement"]["move"]
        dash = player_sheet["movement"]["dash"]
        climb = player_sheet["movement"]["climb"]
        jump_h = player_sheet["movement"]["jump"]["horizontal"]
        jump_v = player_sheet["movement"]["jump"]["vertical"]

        if chained == False:
            if target:
                player = target
            else:
                player = ctx.author
            embed.title = f"Movement Stats :: {player_sheet['name']} ```Player: {player.display_name}```"

        embed.add_field(name="Move", value=f"```{move}```")
        embed.add_field(name="Dash", value=f"```{dash}```")
        embed.add_field(name="Climb", value=f"```{climb}```")
        embed.add_field(
            name="\u200b", value=f"```{yards_to_kph(move)} KmH\n{yards_to_mps(move)} m/s\n{yards_to_mph(move)} MpH```")
        embed.add_field(
            name="\u200b", value=f"```{yards_to_kph(dash)} KmH\n{yards_to_mps(dash)} m/s\n{yards_to_mph(dash)} MpH```")
        embed.add_field(
            name="\u200b", value=f"```{yards_to_kph(climb)} KmH\n{yards_to_mps(climb)} m/s\n{yards_to_mph(climb)} MpH```")
        embed.add_field(name="Jump - Vertical",
                        value=f"```{jump_v} ({yards_to_meters(jump_v)} meters)```")
        embed.add_field(name="Jump - Horizontal",
                        value=f"```{jump_h} ({yards_to_meters(jump_h)} meters)```")

        if ctx.author == self.storyteller and private == True:
            await self.storyteller.send(embed=embed)
        elif private:
            await ctx.author.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.command(aliases=["ab", "rollfor"])
    async def abilityroll(self, ctx, ability: str = None, attr: str = None, private=False, mod: int = 0, target: discord.Member = None):
        def similar(a, b):
            if len(a) > 9:
                a = a[0:8]
            if len(b) > 9:
                b = b[0:8]
            return SequenceMatcher(None, a, b).ratio()

        if str(ctx.author.id) in [config["gamemaster"][0]["ganj"]] and target:
            player_key = target.id
        else:
            player_key = ctx.author.id
            if target:
                await ctx.send("```Only the GM can access other players character sheets.```", delete_after=5.0)

        player_sheet = [
            pc for pc in self.character_roster if pc["player_id"] == player_key][0]
        ability_check = [(a, player_sheet["abilities"][a])
                         for a in player_sheet["abilities"] if similar(a, ability) > 0.6]
        if len(ability_check):
            attr_check = [(a, player_sheet["attributes"][a])
                          for a in player_sheet["attributes"] if similar(a, attr) > 0.6]
            if len(attr_check):
                clogger(f"Rolling for {ability_check}, {attr_check}")
                attr_str = attr_check[0][0]
                attr_val = attr_check[0][1] + player_sheet[f"{attr_str}_mod"]
                ability_str = ability_check[0][0]
                ability_val = ability_check[0][1] + mod
                clogger(
                    f"Raw values - Epic Attr: {player_sheet['epic_attributes'][f'epic_{attr_str}']}")
                clogger(
                    f"Raw values - Epic Attr Mod: {player_sheet[f'epic_{attr_str}_mod']}")
                epic_attr_val = player_sheet['epic_attributes'][f'epic_{attr_str}'] + \
                    player_sheet[f'epic_{attr_str}_mod']
                clogger(f"?roll {ability_val},{attr_val}, {epic_attr_val}")
                await ctx.send(f"\n```markdown\n#> Rolling: {attr_str.title()} ({attr_val}) and {ability_str.title()} ({ability_val})```", delete_after=5.0)
                await Roller.roll(None, ctx, f"{ability_val},{attr_val},{epic_attr_val}", private, self.storyteller)


def setup(client):
    client.add_cog(Character(client))
