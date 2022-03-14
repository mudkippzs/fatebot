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
			"0": [2,1,1], # Legend 0: House ruled to permit more
			"2": [8,6,4], # variety in NPCs. If Legend 0's are
			"5": [4,3,2], # too powerful; tweak.
			"9": [4,3,2],
			"14": [8,6,4],
			"20": [8,6,4],
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
		return self.generate(label, legend, pantheon, god)

	def generate(self, label, legend, pantheon, god):
		self.__generate_random_npc(label, legend, pantheon, god)

	def save_to_dict(self):
		now = datetime.datetime.now()
		timestamp = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%d' % (now.microsecond))

		if self.legend == 1:
			npc_legend_label = f"0{self.legend}"
		else:
			npc_legend_label = f"{self.legend}"

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

		if self.debug is False:
			#dprinter.dp(f"L: {legend}, LOW: {self.legend_lower_constraint} , HIGH: {self.legend_upper_constraint}", "__set_challenge_level")
			self.legend = random.randint(legend - self.legend_lower_constraint, legend + self.legend_upper_constraint)
		else:
			self.legend = legend

		self.template["legend"] = self.legend

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
		random.shuffle(attribute_points)
		if attribute_points[0] > 0:
			#dprinter.dp(f"Legend: {self.legend} - Attributes to spend:{attribute_points}", "randomly_distribute_attributes")
			#dprinter.dp(self.template["attributes"])
			physical = [
				self.template["attributes"]["stre"],
				self.template["attributes"]["dex"],
				self.template["attributes"]["sta"],
			]

			social = [
				self.template["attributes"]["cha"],
				self.template["attributes"]["man"],
				self.template["attributes"]["app"],
			]

			mental = [
				self.template["attributes"]["per"],
				self.template["attributes"]["inte"],
				self.template["attributes"]["wits"],
			]

			random.shuffle(physical)
			random.shuffle(social)
			random.shuffle(mental)

			att_1_total = attribute_points[0]
			att_2_total = attribute_points[1]
			att_3_total = attribute_points[2]

			calc_attr_p_0 = math.ceil(att_1_total / 2)
			calc_attr_p_1 = math.ceil(att_1_total / 4)
			calc_attr_p_2 = math.floor(att_1_total / 4)
			calc_attr_s_0 = math.ceil(att_2_total / 2)
			calc_attr_s_1 = math.ceil(att_2_total / 4 )
			calc_attr_s_2 = math.floor(att_2_total / 4 )
			calc_attr_m_0 = math.ceil(att_3_total / 2)
			calc_attr_m_1 = math.ceil(att_3_total / 4)
			calc_attr_m_2 = math.floor(att_3_total / 4)
					
			physical[0] += calc_attr_p_0
			physical[1] += calc_attr_p_1
			physical[2] += calc_attr_p_2

			
			social[0] += calc_attr_s_0
			social[1] += calc_attr_s_1
			social[2] += calc_attr_s_2

			
			mental[0] += calc_attr_m_0
			mental[1] += calc_attr_m_1
			mental[2] += calc_attr_m_2

			self.template["attributes"]["stre"] = physical[0]
			self.template["attributes"]["dex"] = physical[1]
			self.template["attributes"]["sta"] = physical[2]

			self.template["attributes"]["cha"] = social[0]
			self.template["attributes"]["man"] = social[1]
			self.template["attributes"]["app"] = social[2]

			self.template["attributes"]["per"] = mental[0]
			self.template["attributes"]["inte"] = mental[1]
			self.template["attributes"]["wits"] = mental[2]

			#dprinter.dp(self.template["attributes"])

		return

		
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
			boon_list.append(boons.choose_boons_by_level(self.template, purview))
		boon_list = [boon for sublist in boon_list for boon in sublist]
		for point in range(budget):
			taken = [b[0] for b in self.template["boons"]]
			if len(boon_list):
				random_boon = random.choice(boon_list)
				if random_boon[0] not in taken:
					self.template["boons"].append(random_boon)

		return

	def __choose_knacks(self):
		self.template = knacks.choose_random_knacks(self.template, self.god_data, self.new_knacks)
		
		return

	def __choose_virtues(self):
		if "god" in self.template.keys():
			pantheon = self.template["pantheon"]
			self.template["virtues"] = [random.randint(0, 3), random.randint(0,2), random.randint(0, 1), random.randint(0, 1)]

		return

	def __choose_epic_attributes(self, budget, inital=True):
		attr_list = []
		loop_limit = 30
		for attribute in self.template["attributes"]:
			attr_list.append([attribute, self.template["attributes"][attribute]])

		max_attr = []
		for l in attr_list:
			if len(max_attr):
				if l[1] > max_attr[1]:
					max_attr = l
			else:
				max_attr = l
		parents_favoured = self.god_data["favoured"]["epic_attributes"]
		
		attribute_list = [[k,v] for k,v in enumerate(self.template["epic_attributes"])]
		
		while budget > 0:
			attribute = random.choice(attribute_list)[1]
			standard_attribute = attribute.replace("epic_","")
			#dprinter.dp(f"EA Budget: {budget}, Attr: {attribute}", "__choose_epic_attributes")
			
			if attribute in parents_favoured:
				if (budget - (self.template["epic_attributes"][attribute] * 4)) > 0:
					if (self.template["epic_attributes"][attribute] + 1) <= self.legend and (self.template["epic_attributes"][attribute] + 1) < self.template["attributes"][standard_attribute]:
						budget -= self.template["epic_attributes"][attribute] * 4
						self.template["epic_attributes"][attribute] += 1
						self.new_knacks[attribute.replace("epic_", "")] += 1
			elif (budget - (self.template["epic_attributes"][attribute] * 5)) > 0:
				if random.randint(0, 1) == True:
					if (self.template["epic_attributes"][attribute] + 1) <= self.legend and (self.template["epic_attributes"][attribute] + 1) < self.template["attributes"][standard_attribute]:
						budget -= self.template["epic_attributes"][attribute] * 5
						self.template["epic_attributes"][attribute] += 1
						self.new_knacks[attribute.replace("epic_", "")] += 1
			else:
				#ea_val = self.template["epic_attributes"][attribute]
				#dprinter.dp(f"Budget is {budget} - breaking loop. - EA: {ea_val}")
				break

			loop_limit -= 1
			if loop_limit <= 0:
				break

		#pp(self.template)				
		
		return budget

	def __apply_experience(self, legend):
		self.__set_legend(legend)
		

		if legend > 1:
			#xp_list = growths.quadratic_increase(15)
			xp_list = [0,0,15,0,0,15,0,0,0,20,0,0,0,0,20,0,0,0,0,0,20,0,0,0]
			total_points = xp_list[legend]
			
			if total_points > 0:
				self.__randomly_distribute_attributes()
				if total_points >= 2:
					boon_budget = random.randint(1, math.ceil(total_points / 2))
				else:
					boon_budget = 1

				ea_budget = total_points - boon_budget
				
				if ea_budget > 0:
					self.__choose_epic_attributes(ea_budget, inital=False)
					self.__choose_knacks()
				
				if boon_budget > 0:
					self.__choose_boons(boon_budget)
					
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
		self.__set_legend(0)
		self.__choose_virtues()

		self.__choose_abilites()
		self.__randomly_distribute_attributes()
		self.new_knacks = {
			"stre": 0,
			"dex": 0,
			"sta": 0,
			"cha": 0,
			"man": 0,
			"app": 0,
			"per": 0,
			"inte": 0,
			"wits": 0,
		}

		if self.legend >= 1:

			current_boon_count = len(self.template["boons"])
			total_boon_knack_budget = 15
			boon_budget = random.randint(1, math.ceil(total_boon_knack_budget / 2))
			
			ea_budget = total_boon_knack_budget - boon_budget
			
			self.__choose_boons(boon_budget)
			self.__choose_epic_attributes(ea_budget)
			self.__choose_knacks()

		for legend in range(final_legend + 1):
			self.__apply_experience(legend)

		self.__generate_name()

		self.player = Player(f"{self.discord_tag} - {self.name}", config["gamemaster"][0]["ganj"], True, self.legend, self.template)

		return

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