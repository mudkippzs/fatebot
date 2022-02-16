from pprint import pprint as pp
from copy import deepcopy

from characters import pc_bob 
from characters import pc_vasily 
from characters import pc_jean 
from characters import pc_set 
from characters import pc_set_ferdiad 
from characters import pc_set_standard_summon

import nature
import knacks
import boons
import growths

from pantheons import get_random_pantheon_god
from pantheons import search_gods
from pantheons import get_virtues

from npcs import npc_template

import matplotlib.pyplot as plt

from epiccalc import calculate_epic
from main import rolldice

import argparse
import datetime
import json
import math
import pathlib
import random

import namegenerator

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


def randomly_distribute_attributes(character_data, legend):
	
	#print(f" Total points to distriubte: {total_points}")

	attribute_dict = {
		"0": [2,2,1],
		"1": [0,0,0],
		"2": [8,6,4],
		"3": [0,0,0],
		"4": [0,0,0],
		"5": [4,3,2],
		"6": [0,0,0],
		"7": [0,0,0],
		"8": [0,0,0],
		"9": [4,3,2],
		"10": [0,0,0],
		"11": [0,0,0],
		"12": [0,0,0],
		"13": [0,0,0],
		"14": [4,3,2],
		"15": [0,0,0],
		"16": [0,0,0],
		"17": [0,0,0],
		"18": [0,0,0],
		"19": [0,0,0],
		"20": [4,3,2],
	}

	#pp(f"Attribute dict: {attribute_dict[str(legend)]}")

	attribute_order = attribute_dict[str(legend)]

	for _ in range(1, 10):
		random.shuffle(attribute_order)
	
	# print(attribute_order)
	attr_order = [
		attribute_order[0],
		attribute_order[1],
		attribute_order[2],
	]

	random.shuffle(attr_order)

	attributes = [
		[0,0,0],
		[0,0,0],
		[0,0,0],
	]

	count = 0
	for idx, attrs in enumerate(attributes):
		total_points = attr_order[count]

		first_attr_to_add = math.ceil(total_points / 4)
		attrs[0] += first_attr_to_add
		total_points -= attrs[0] 
		
		second_attr_to_add = math.ceil(total_points / 2)
		attrs[1] += math.ceil(total_points / 2)
		total_points -= attrs[1]

		attrs[2] += total_points

		total_attrs = sum([attrs[0], attrs[1], attrs[2]])
		
		#print(f" Attrs: ({total_attrs}) 1st: {first_attr_to_add}, 2nd: {second_attr_to_add}, 3rd: {total_points}")

		#if total_points != 0:
		#	print(f" Remaining points greater than 0: {total_points}")

		attributes[idx][0] += attrs[0]
		attributes[idx][1] += attrs[1]
		attributes[idx][2] += attrs[2]

		count += 1

	character_data["attributes"]["stre"] += attributes[0][0]
	character_data["attributes"]["dex"] += attributes[0][1]
	character_data["attributes"]["sta"] += attributes[0][2]
	character_data["attributes"]["cha"] += attributes[1][0]
	character_data["attributes"]["man"] += attributes[1][1]
	character_data["attributes"]["app"] += attributes[1][2]
	character_data["attributes"]["per"] += attributes[2][0]
	character_data["attributes"]["inte"] += attributes[2][1]
	character_data["attributes"]["wits"] += attributes[2][2]	

	return character_data

def choose_abiliites(character_data, god_data):
	total_points = 30
	parents_favoured = god_data["favoured"]["abilities"]
	for favoured in parents_favoured:
		spend = random.randint(1,3)
		favoured_ability = favoured.lower().replace(" ", "_").split("_(")[0]
		try:
			character_data["abilities"][favoured_ability] += spend
		except KeyError as e:
			print(favoured_ability)
			print(character_data["abilities"])
			raise e
		total_points -= spend

	for ability in character_data["abilities"]:
		ability = ability.lower().replace(" ", "_")
		if character_data["abilities"][ability] < 3:
			character_data["abilities"][ability] += random.randint(0, 3 - character_data["abilities"][ability])
	
	return character_data

def choose_boons(character_data, god_data, boon_budget):
	boon_list = []
	pantheon = character_data["pantheon"]
	for purview in god_data["favoured"]["purviews"]:
		#print(f"Getting boons for purview: {purview}")
		boon_list.append(boons.get_boons_by_level(character_data["legend"], purview))
	boon_list = [boon for sublist in boon_list for boon in sublist]
	if len(boon_list):
		taken = []
		for point in range(0, boon_budget):
			random_index = random.randint(0, len(boon_list) - 1)
			if random_index not in taken:
				choice_boon = boon_list[random_index]
				character_data["boons"].append(choice_boon)
				taken.append(random_index)
	
	return character_data

def choose_knacks(character_data, god_data, knack_budget):
	while knack_budget > 0:
		for attr in [a.replace("epic_","") for a in character_data["epic_attributes"]]:
			knack_count_before = len(character_data["knacks"])
			character_data = knacks.get_all_knacks_by_attr(attr, character_data, god_data)
			knack_count_after = len(character_data["knacks"])
			knack_budget = knack_budget - 1
			#print(f"Spent a knack point, points remaining: {knack_budget}")

	return character_data


def choose_virtues(character_data):
	if "god" in character_data.keys():
		pantheon = character_data["pantheon"]
		character_data["virtues"] = [random.randint(0, 3), random.randint(0,2), random.randint(0, 1), random.randint(0, 1)]

	return character_data

def choose_epic_attributes(character_data, god_data, ea_budget):
	attr_list = []
	for attribute in character_data["attributes"]:
		attr_list.append([attribute, character_data["attributes"][attribute]])

	max_attr = []
	for l in attr_list:
		if len(max_attr):
			if l[1] > max_attr[1]:
				max_attr = l
		else:
			max_attr = l
	#print(f"Total Epic Attribute Points: {ea_budget}")
	parents_favoured = god_data["favoured"]["epic_attributes"]
	#pp(character_data["epic_attributes"])
	while ea_budget > 0 :
		for _ in range(0, ea_budget):
			attribute = random.choice([[k,v] for k,v in enumerate(character_data["epic_attributes"])])[1]
			character_data["epic_attributes"][attribute] += 1
			ea_budget = ea_budget - 1
			
	#pp(character_data)				
	
	return character_data

def apply_experience(character_data, god_data, legend):
	if legend > 1:
		#xp_list = growths.quadratic_increase(15)
		xp_list = [0,0,15,0,0,15,0,0,0,15,0,0,0,0,15,0,0,0,0,0,15,0,0,0]
		total_points = xp_list[legend]
		
		character_data = randomly_distribute_attributes(character_data, legend)
		character_data = choose_epic_attributes(character_data, god_data, total_points)
		
		#print(f"== Total points: {total_points}")
		while total_points > 0:
			boon_budget = math.ceil(total_points * 0.20)
			knack_budget = math.ceil(total_points * 0.20)

			total_points -= boon_budget
			total_points -= knack_budget

			if boon_budget >= 1:
				character_data = choose_boons(character_data, god_data, boon_budget)
			
			if knack_budget >= 1:
				character_data = choose_knacks(character_data, god_data, knack_budget)
				
	return character_data


def generate_random_npc(name, challenge_level, npc_template_copy, pantheon=None, god=None):
	

	#random_challenge_level = random.randint(challenge_level -1, challenge_level +1)
	random_challenge_level = challenge_level
	if random_challenge_level < 0:
		random_challenge_level = 0

	npc_template_copy["nature"] = random.choice(nature.NATURE)
	npc_template_copy["legend"] = random_challenge_level

	legend = npc_template_copy["legend"]

	npc_template_copy = randomly_distribute_attributes(npc_template_copy, 0)

	if god:
		search_gods(god)
	elif pantheon:
		god, pantheon, god_data = get_random_pantheon_god(pantheon)
	else:
		god, pantheon, god_data = get_random_pantheon_god()

	if legend > 0:
		npc_template_copy["god"] = god
		npc_template_copy["pantheon"] = pantheon
	else:
		npc_template_copy["god"] = "None"
		npc_template_copy["pantheon"] = "None"

	#print(f"Generating a Scion of {god} from {pantheon} at Legend: {legend}")

	npc_template_copy = choose_abiliites(npc_template_copy, god_data)
	
	boon_knack_budget = [0, 0]
	
	for point in range(1, 11):
		random.shuffle(boon_knack_budget) 
		boon_knack_budget[0] += 1

	boon_budget = boon_knack_budget[0]
	ea_budget = boon_knack_budget[1]

	#print(f"Boon Budget: {boon_budget} - Epic Attr Budget: {ea_budget}")
	if legend >= 1:
		npc_template_copy = choose_boons(npc_template_copy, god_data, boon_budget)
		npc_template_copy = choose_epic_attributes(npc_template_copy, god_data, ea_budget)
		npc_template_copy = choose_knacks(npc_template_copy, god_data, ea_budget)
		npc_template_copy = choose_virtues(npc_template_copy)

	for lp in range(1, npc_template_copy["legend"]):
		npc_template_copy = apply_experience(npc_template_copy, god_data, lp)	

	npc = Player(name, config["gamemaster"][0]["ganj"], True, npc_template_copy["legend"], npc_template_copy)
	
	return npc, npc_template_copy

def legend_bumper():
    i = 0
    while True:
        yield i
        i += 1
        if i>12:
        	i = 0

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="NPC Generator for Scion 1e.")
	parser.add_argument('--generate_npc','-n', type=int)
	parser.add_argument('--test','-t', action='store_true')
	args = parser.parse_args()

	# Players

	bob_joe = Player("Bob",config["players"][0]["bob"], False, 3, pc_bob.PLAYER_CHARACTER_SHEET)
	vasily_tom = Player("Vasily Volkov",config["players"][0]["vasily"], False, 3, pc_vasily.PLAYER_CHARACTER_SHEET)
	jean_potato = Player("Jeanne Chadwick",config["players"][0]["jean"], False, 3, pc_jean.PLAYER_CHARACTER_SHEET)
	set_liddy = Player("Set", config["players"][0]["set"], False, 3, pc_set.PLAYER_CHARACTER_SHEET)
	set_ferdiad = Player("Ferdiad (Set's Summon)", config["players"][0]["set"], False, 3, pc_set_ferdiad.PLAYER_CHARACTER_SHEET)
	set_standard_summon = Player("Fianna Warrior (Set's Summon)", config["players"][0]["set"], False, 3, pc_set_standard_summon.PLAYER_CHARACTER_SHEET)
	npc_gen_flag = args.generate_npc if args.generate_npc else 0

	if npc_gen_flag > 0:
		# NPCs
		country_dict = {
			"Pesedjet": ["EG", "EG", "US"],
			"Dodekatheon": ["GR", "IT", "GR", "US"],
			"Aesir": ["DE", "FI", "NO", "US", "IE"],
			"Atzlanti": ["MX", "ES", "US"],
			"Amatsukami": ["JP", "US"],
			"Loa": ["FR", "FR", "FR", "US"],
			"Tuatha": ["IE", "IE", "IE", "US"],
			"Celestial Bureaucracy": ["TW", "TW", "CN"],
			"Devas": ["IN",],
			"Yazata": ["IR", "IQ", "AZ", "YE"],
			"Atlantean": ["GR", "IT"],
			"None": ["US", "IE", "ES", "DE", "JP", "FR", "IT", "US"]
		}

		l = legend_bumper()

		#print("Name| God | Pantheon | Legend|Attrs[>\t\t\tSTR | DEX | STA || CHA | MAN | APP || PER | INT | WIT ]")
		for _ in range(0, npc_gen_flag):
			template = deepcopy(npc_template.PLAYER_CHARACTER_SHEET)
			npc, npc_dict = generate_random_npc(name=None, challenge_level=next(l), npc_template_copy=template)
			
			if npc.name is None:
				if npc.pantheon:
					random_country = random.choice(country_dict[npc.pantheon])
				else:
					random_country = random.choice(country_dict["None"])

				random_gender = random.choice(["Male", "Male", "Female"])

				first_name_list = namegenerator.get_random_first_names_by_country(random_country, random_gender)
				last_name_list = namegenerator.get_random_last_names_by_country(random_country)
				f_name = random.choice(first_name_list[random_country][random_gender[0]])
				l_name = random.choice(last_name_list[random_country])
				npc.name = f"{f_name} {l_name}"
				npc_dict["name"] = npc.name

			stre = npc.attributes["stre"]
			dex = npc.attributes["dex"]
			sta = npc.attributes["sta"]
			cha = npc.attributes["cha"]
			man = npc.attributes["man"]
			app = npc.attributes["app"]
			per = npc.attributes["per"]
			inte = npc.attributes["inte"]
			wit = npc.attributes["wits"]

			print(f"{npc.legend} | \n\tSTR {stre} |DEX {dex} |STA {sta}\n\tCHA {cha} |MAN {man} |APP {app}\n\tPER {per} |INT {inte} |WIT {wit}")
			# count += 1
			# print(f"{npc.name}, a Scion of {npc.god}")
			# pp(npc.name)
			# pp(npc.discord_tag)
			# pp(npc.pantheon)
			# pp(npc.god)
			# pp(npc.legend)
			# pp(npc.nature)
			# pp(npc.attributes)
			# pp(npc.epic_attributes)
			# pp(npc.abilities)
			# pp(npc.knacks)
			# pp(npc.boons)
			# pp(npc.relics)
			# pp(npc.combat)
			# pp(npc.movement)
			now = datetime.datetime.now()
			timestamp = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%d' % (now.microsecond))
			
			if len(str(npc.legend)) == 1:
				npc_legend_label = f"0{npc.legend}"
			npc_path = pathlib.Path(f"/home/dev/Code/fatebot/npcs/generated/{npc_legend_label}/")
			npc_path.mkdir(parents=True, exist_ok=True)
			
			if npc.legend:			
				npc_path = pathlib.Path(f"/home/dev/Code/fatebot/npcs/generated/{npc_legend_label}/{npc.name}_{npc.pantheon}_{npc.god}_{timestamp}.json")
			else:
				npc_path = pathlib.Path(f"/home/dev/Code/fatebot/npcs/generated/{npc_legend_label}/{npc.name}_NPC_{timestamp}.json")


			with open(npc_path, "w") as f:
				json.dump(npc_dict, f, indent=4)

	band = [
		bob_joe,
		vasily_tom,
		jean_potato,
		set_liddy,
	]

