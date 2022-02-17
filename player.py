from pprint import pprint as pp
from copy import deepcopy

import matplotlib.pyplot as plt

from epiccalc import calculate_epic
from main import rolldice

import argparse
import datetime
import json
import math
import random

with open("config.json", "r") as f:
    config = json.load(f)

class Player:
	name = None
	npc = False
	god = []
	pantheon = []
	xp_total = 0
	xp_spent = 0
	bonus_points = 0
	stunt_log = []


	def __init__(self, name: str =None, discord_tag: str=None, npc: bool=None, legend: int=0, options:dict={}):
		self.name = name
		self.discord_tag = discord_tag
		self.npc = npc,
		self.legend = legend
		for key, value in enumerate(options):
			setattr(self, str(value), options[value])
		self.setup_character()

	def setup_character(self):
		self.setup_legend()
		self.setup_willpower()
		self.recalculate_vitals()
		# pp(vars(self))

	def recalculate_vitals(self):
		self.setup_movement()
		self.setup_combat()
		self.setup_soak()

	def setup_legend(self):
		self.legend_points_total = self.legend * self.legend
		self.legend_points_current = self.legend_points_total
		return

	def setup_willpower(self):
		willpower_calc = sorted(self.virtues, key=None, reverse=True)[0:2]
		self.willpower_total = sum(willpower_calc)
		self.willpower_current = self.willpower_total
		return

	def add_legend(self, value=1):
		if value < 0:
			value = value * -1
		self.legend_points_current += value
		return

	def remove_legend(self, value=1):
		if value < 0:
			value = value * -1
		self.legend_points_current -= value
		return

	def add_willpower(self, value=1):
		if value < 0:
			value = value * -1
		self.willpower_current += value
		return

	def remove_willpower(self, value=1):
		if value < 0:
			value = value * -1
		self.willpower_current -= value
		return

	def add_xp(self, value=1):
		if value < 0:
			value = value * -1
		self.xp_total += value
		return

	def join_battle(self):
		self.join_battle = 0
		
		wits = self.attributes["wits"]
		wits_epic = self.epic_attributes["epic_wits"]
		wits_mod = self.wits_mod
		awareness = self.abilities["awareness"]

		roll_string = f"{wits + wits_mod},{awareness},{wits_epic}"
		dice_log = []
		dice_results, successes, extra_successes, success_total = rolldice(roll_string)
		self.join_battle = success_total
		
		# To debug dice JB rolls - uncomment. @TODO: Refactor into a debugger.

		# for i in range(1,100):
		# 	dice_results, successes, extra_successes, success_total = rolldice(roll_string)
		# 	dice_log.append(success_total)
		# print(dice_log)

		return success_total

	def __string_stripper(self, string):
		filter_string = string.lower().translate({ord(c): "" for c in "!@#$%^&*()'[]{};:,./<>?\|`~-=_+"})
		return filter_string

	def use_boon(self, boon):
		if len(boon):
			for player_boon in self.boons:
				b = self.__string_stripper(boon)
				pb = self.__string_stripper(player_boon)
				if b in pb:
					return player_boon
			return f"You don't have boon: \"{boon}\"." # @TODO: create a string table for all these strings
		return f"No search term given for `boon`. Please try again!"

	def use_knack(self, knack):
		if len(knack):
			for player_knack in self.knacks:
				k = self.__string_stripper(knack)
				pk = self.__string_stripper(player_knack)
				if k in pk:
					return player_knack
			return f"You don't have a knack named: {knack}." # @TODO: create a string table for all these strings
		return f"No search term given for `knack`. Please try again!"

	def setup_movement(self):
		self.movement["move"] = self.attributes["dex"] + calculate_epic(self.epic_attributes["epic_dex"])
		self.movement["dash"] = self.attributes["dex"] + 6 + calculate_epic(self.epic_attributes["epic_dex"])
		self.movement["jump"]["vertical"] = self.abilities["athletics"] + self.attributes["stre"] + calculate_epic(self.epic_attributes["epic_stre"])
		self.movement["jump"]["horizontal"] = self.movement["jump"]["vertical"] * 2
		self.movement["climb"] = self.attributes["stre"] +  calculate_epic(self.epic_attributes["epic_stre"])
		return

	def setup_combat(self):
		# Dodge DV Dexterity + Athletics + Legend) / 2
		self.combat["dodge_dv"] = math.ceil((self.legend + self.abilities["athletics"] + self.attributes["dex"] + calculate_epic(self.epic_attributes["epic_dex"]) / 2))
		# Parry DV Dexterity + Brawl or Melee + weapon’s Defense) / 2
		parry_combat_value = self.abilities["brawl"] if self.abilities["brawl"] >= self.abilities["melee"] else self.abilities["melee"]
		self.combat["parry_dv"] =  math.ceil(parry_combat_value + self.attributes["dex"] + calculate_epic(self.epic_attributes["epic_dex"]) / 2)
		return

	def setup_soak(self):
		self.soak["bludgeon"] = self.attributes["sta"] + calculate_epic(self.epic_attributes["epic_sta"])
		self.soak["lethal"] = (self.soak["bludgeon"] / 2) + calculate_epic(self.epic_attributes["epic_sta"])
		pass



if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Player Generator for Scion 1e.")
	args = parser.parse_args()

	# Players

	bob_joe = Player("Bob",config["players"][0]["bob"], False, 3, pc_bob.PLAYER_CHARACTER_SHEET)
	vasily_tom = Player("Vasily Volkov",config["players"][0]["vasily"], False, 3, pc_vasily.PLAYER_CHARACTER_SHEET)
	jean_potato = Player("Jeanne Chadwick",config["players"][0]["jean"], False, 3, pc_jean.PLAYER_CHARACTER_SHEET)
	set_liddy = Player("Set", config["players"][0]["set"], False, 3, pc_set.PLAYER_CHARACTER_SHEET)
	set_ferdiad = Player("Ferdiad (Set's Summon)", config["players"][0]["set"], False, 3, pc_set_ferdiad.PLAYER_CHARACTER_SHEET)
	set_standard_summon = Player("Fianna Warrior (Set's Summon)", config["players"][0]["set"], False, 3, pc_set_standard_summon.PLAYER_CHARACTER_SHEET)
	
