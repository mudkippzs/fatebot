# Built-ins
from copy import deepcopy
from pprint import pprint as pp

import argparse
import datetime
import json
import math
import pathlib
import random

# Data deps.
import pantheons
import nature
import knacks
import boons
import pantheons  

# Class deps
from player import Player

# Util functions.
from dprint import Dprint
from main import rolldice
from npcs import npc_template

import growths
import epiccalc
import namegenerator

# Setup debug logger
dprinter = Dprint()

# Get our config vals.
with open("config.json", "r") as f:
    config = json.load(f)

def calculate_attribute_points(legend):
	# Attributes can only be increased at certain legend ranks. 
	# Otherwise they should have 0 points to spend.
	attribute_point_set = [0,0,0]
	
	if legend in [0, 2, 5, 9, 14, 20]:
		attribute_point_dict = {
			"0": [2,2,1], # Legend 0: House ruled to permit more
			"2": [8,6,4], # variety in NPCs. If Legend 0's are
			"5": [4,3,2], # too powerful; tweak.
			"9": [4,3,2],
			"14": [4,3,2],
			"20": [4,3,2],
		}
		attribute_point_set = attribute_point_dict[str(legend)]
	
	return attribute_point_set

class NPC:

	# Config values that tweak the math of NPC generation.

	# Multipler for legend rating when randomly generating NPCs.
	legend_lower_constraint = 1
	legend_upper_constraint = 1


	def __init__(self, label="Random NPC", legend=2, template:dict = npc_template.PLAYER_CHARACTER_SHEET, pantheon:str =None, god:str =None, bonus_xp:int = 0, debug:bool =False):
		self.debug = debug
		# Clone the npc template dictionary, this ensures the root dict isn't shared between objects.
		self.template = deepcopy(npc_template.PLAYER_CHARACTER_SHEET)
		self.generate(label, legend, pantheon, god)

	def generate(self, label, legend, pantheon, god):
		self.__generate_random_npc(label, legend, pantheon, god)

	def save_to_dict(self):
		now = datetime.datetime.now()
		timestamp = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%d' % (now.microsecond))
		
		if len(str(self.legend)) == 1:
			npc_legend_label = f"0{self.legend}"
		npc_path = pathlib.Path(f"/home/dev/Code/fatebot/npcs/generated/{npc_legend_label}/")
		npc_path.mkdir(parents=True, exist_ok=True)
		
		if self.legend:			
			npc_path = pathlib.Path(f"/home/dev/Code/fatebot/npcs/generated/{npc_legend_label}/{self.name}_{self.pantheon}_{self.god}_{timestamp}.json")
		else:
			npc_path = pathlib.Path(f"/home/dev/Code/fatebot/npcs/generated/{npc_legend_label}/{self.name}_NPC_{timestamp}.json")


		with open(npc_path, "w") as f:
			json.dump(self.template, f, indent=4)

		return

	def __set_legend(self, legend):
		if legend < 0:
			legend = 0
		elif legend > 20:
			legend = 20

		if self.debug is True:
			dprinter.dp(f"L: {legend}, LOW: {self.legend_lower_constraint} , HIGH: {self.legend_upper_constraint}", "__set_challenge_level")
			self.legend = random.randint(legend - self.legend_lower_constraint, legend + self.legend_upper_constraint)
		else:
			self.legend = legend

		self.template["legend"] = legend

		return

	def __set_divinity(self, god, pantheon, legend):
		if legend:
			self.god = None
			self.pantheon = None

			if god:
				pantheons.search_gods(god)
			elif pantheon:
				self.god, self.pantheon, self.god_data = pantheons.get_random_pantheon_god(pantheon)
			else:
				self.god, self.pantheon, self.god_data = pantheons.get_random_pantheon_god()
			
			self.template["god"] = self.god
			self.template["pantheon"] = self.pantheon

			return True

		return False

	def __randomly_distribute_attributes(self):
		attribute_points = calculate_attribute_points(self.legend)
		dprinter.dp(f"Legend: {self.legend} - Attributes to spend:{attribute_points}", "randomly_distribute_attributes")
		
	def __set_nature(self):
		random_nature = random.choice(nature.NATURE)
		if len(random_nature):
			self.template["nature"] = random_nature
			return True
		return False

	def __choose_abilites(self):
		total_points = 30
		parents_favoured = self.god_data["favoured"]["abilities"]
		for favoured in parents_favoured:
			spend = random.randint(1,3)
			favoured_ability = favoured.lower().replace(" ", "_").split("_(")[0]
			try:
				self.template["abilities"][favoured_ability] += spend
			except KeyError as e:
				print(favoured_ability)
				print(self.template["abilities"])
				raise e
			total_points -= spend

		for ability in self.template["abilities"]:
			ability = ability.lower().replace(" ", "_")
			if self.template["abilities"][ability] < 3:
				self.template["abilities"][ability] += random.randint(0, 3 - self.template["abilities"][ability])
		
		return

	def __choose_boons(self, budget):
		boon_list = []
		pantheon = self.pantheon
		for purview in self.god_data["favoured"]["purviews"]:
			#print(f"Getting boons for purview: {purview}")
			boon_list.append(boons.get_boons_by_level(self.template["legend"], purview))
		boon_list = [boon for sublist in boon_list for boon in sublist]
		if len(boon_list):
			taken = []
			for point in range(0, budget):
				random_index = random.randint(0, len(boon_list) - 1)
				if random_index not in taken:
					choice_boon = boon_list[random_index]
					self.template["boons"].append(choice_boon)
					taken.append(random_index)
		return

	def __choose_knacks(self, budget):
		while budget > 0:
			for attr in [a.replace("epic_","") for a in self.template["epic_attributes"]]:
				knack_count_before = len(self.template["knacks"])
				self.template = knacks.get_all_knacks_by_attr(attr, self.template, self.god_data)
				knack_count_after = len(self.template["knacks"])
				budget = budget - 1
				#print(f"Spent a knack point, points remaining: {budget}")

		return

	def __choose_virtues(self):
		if "god" in self.template.keys():
			pantheon = self.template["pantheon"]
			self.template["virtues"] = [random.randint(0, 3), random.randint(0,2), random.randint(0, 1), random.randint(0, 1)]

		return

	def __choose_epic_attributes(self, budget):
		attr_list = []
		for attribute in self.template["attributes"]:
			attr_list.append([attribute, self.template["attributes"][attribute]])

		max_attr = []
		for l in attr_list:
			if len(max_attr):
				if l[1] > max_attr[1]:
					max_attr = l
			else:
				max_attr = l
		#print(f"Total Epic Attribute Points: {budget}")
		parents_favoured = self.god_data["favoured"]["epic_attributes"]
		#pp(self.template["epic_attributes"])
		dprinter.dp(f"preloop EA Budget: {budget}", "__choose_epic_attributes")
		while budget > 0 :
			dprinter.dp(f"EA Budget: {budget}", "__choose_epic_attributes")
			attribute = random.choice([[k,v] for k,v in enumerate(self.template["epic_attributes"])])[1]
			if self.template["epic_attributes"][attribute] <= self.legend:
				self.template["epic_attributes"][attribute] += 1
				budget -= 1
				
		#pp(self.template)				
		
		return

	def __apply_experience(self, legend):
		if legend > 1:
			#xp_list = growths.quadratic_increase(15)
			xp_list = [0,0,15,0,0,15,0,0,0,15,0,0,0,0,15,0,0,0,0,0,15,0,0,0]
			total_points = xp_list[legend]
			
			self.__randomly_distribute_attributes()
			boon_budget = math.ceil(total_points * 0.5)
			knack_budget = math.floor(total_points * 0.5)
			
			self.__choose_epic_attributes(knack_budget)
			#print(f"== Total points: {total_points}")
			while total_points > 0:

				dprinter.dp(f"Boon budget: {boon_budget}")
				dprinter.dp(f"Knack budget: {knack_budget}")
				dprinter.dp(f"Total budget: {knack_budget}")

				total_points -= boon_budget
				total_points -= knack_budget

				if boon_budget >= 1:
					self.__choose_boons(boon_budget)
				
				if knack_budget >= 1:
					self.__choose_knacks(knack_budget)
					
		return

	def __generate_name(self):

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

	
		if self.pantheon:
			random_country = random.choice(country_dict[self.pantheon])
		else:
			random_country = random.choice(country_dict["None"])

		random_gender = random.choice(["Male", "Male", "Female"])

		first_name_list = namegenerator.get_random_first_names_by_country(random_country, random_gender)
		last_name_list = namegenerator.get_random_last_names_by_country(random_country)

		f_name = random.choice(first_name_list[random_country][random_gender[0]])
		l_name = random.choice(last_name_list[random_country])

		self.name = f"{f_name} {l_name}"
		self.template["name"] = self.name

	def __generate_random_npc(self, label, final_legend, pantheon=None, god=None):
		self.discord_tag = label
		self.__set_nature()
		self.__set_divinity(god, pantheon, final_legend)
		self.__choose_abilites()

		for legend in range(0, final_legend):
			self.__set_legend(legend)
			self.__randomly_distribute_attributes()

			current_boon_count = len(self.template["boons"])
			boon_budget = 15 
			ea_budget = 8

			#print(f"Boon Budget: {boon_budget} - Epic Attr Budget: {ea_budget}")
			if legend >= 1:
				self.__choose_boons(boon_budget)
				self.__choose_epic_attributes(ea_budget)
				self.__choose_knacks(ea_budget)
				self.__choose_virtues()

			for lp in range(1, self.template["legend"]):
				self.__apply_experience(lp)

			self.__generate_name()

		self.player = Player(f"{self.discord_tag} - {self.name}", config["gamemaster"][0]["ganj"], True, self.legend, self.template)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", "-d", action="store_true")
	parser.add_argument("--count", "-c", type=int)
	parser.add_argument("--legend", "-l", type=int)

	args = parser.parse_args()
	legend = 2
	count = 1

	if args.legend:
		legend = args.legend

	if args.count:
		count = args.count

	for _ in range(0, count):
		n = NPC(legend=legend, debug=True)
		n.save_to_dict()