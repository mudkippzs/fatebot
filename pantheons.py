from dprint import Dprint
import random

from pantheonlist import PANTHEONS

def get_virtues(pantheon):
	if pantheon in PANTHEONS.keys():
		return PANTHEONS[pantheon]["virtues"]


def search_gods(term):
	for pantheon in PANTHEONS:
		for god in PANTHEONS[pantheon]["gods"]:
			if term.lower() in god.lower():
				god_dict = {
				"name": god.title(),
				"pantheon": pantheon.title(),
				"aka": PANTHEONS[pantheon]["gods"][god]["aka"],
				"description": PANTHEONS[pantheon]["gods"][god]["description"],
				"rivals": PANTHEONS[pantheon]["gods"][god]["rivals"],
				"favoured": PANTHEONS[pantheon]["gods"][god]["favoured"],
				}
				return god_dict
	return

def search_pantheon(term):
	pantheon_list = {}  
	for pantheon in PANTHEONS:
		if term.lower() in pantheon.lower():
			pantheon_list[pantheon] = []
			for god in PANTHEONS[pantheon]["gods"]:
				god_dict = {
						"name": god.title(),
						"pantheon": pantheon.title(),
						"aka": PANTHEONS[pantheon]["gods"][god]["aka"],
						"description": PANTHEONS[pantheon]["gods"][god]["description"],
						"rivals": PANTHEONS[pantheon]["gods"][god]["rivals"],
						"favoured": PANTHEONS[pantheon]["gods"][god]["favoured"],
						}
				pantheon_list[pantheon].append(god_dict)
	return pantheon_list

def search_rivals(term):
	rival_list = []
	for pantheon in PANTHEONS:
		for god in PANTHEONS[pantheon]["gods"]:
			if "rivals" in PANTHEONS[pantheon]["gods"][god].keys():
				rivals = [r.lower() for r in PANTHEONS[pantheon]["gods"][god]["rivals"]]
				#Dprint.dp(f"{god}: {rivals}")
				for rival in rivals:
					if term.lower() in rival:
						god_dict = {
							"name": god.title(),
							"pantheon": pantheon.title(),
							"aka": PANTHEONS[pantheon]["gods"][god]["aka"],
							"description": PANTHEONS[pantheon]["gods"][god]["description"],
							"rivals": PANTHEONS[pantheon]["gods"][god]["rivals"],
							"favoured": PANTHEONS[pantheon]["gods"][god]["favoured"],
							}
						rival_list.append(god_dict)

	return rival_list

def search_favoured(term):
	favoured_god = []   
	for pantheon in PANTHEONS:
		for god in PANTHEONS[pantheon]["gods"]:
			if "favoured" in PANTHEONS[pantheon]["gods"][god].keys():
				favoured_abilities = [f for f in PANTHEONS[pantheon]["gods"][god]["favoured"]["abilities"] if f.lower().startswith(term.lower())]
				favoured_epic_attributes = [f for f in PANTHEONS[pantheon]["gods"][god]["favoured"]["epic_attributes"] if f.lower().startswith(term.lower())]
				favoured_purviews = [f for f in PANTHEONS[pantheon]["gods"][god]["favoured"]["purviews"] if f.lower().startswith(term.lower())]
				
				if len(favoured_abilities) > 0 or len(favoured_epic_attributes) > 0 or len(favoured_purviews) > 0:
					god_dict = {
					"name": god.title(),
					"pantheon": pantheon.title(),
					"aka": PANTHEONS[pantheon]["gods"][god]["aka"],
					"description": PANTHEONS[pantheon]["gods"][god]["description"],
					"rivals": PANTHEONS[pantheon]["gods"][god]["rivals"],
					"favoured": PANTHEONS[pantheon]["gods"][god]["favoured"],
					}
					favoured_god.append(god_dict)
	return favoured_god


def get_random_pantheon_god(pantheon=None):
	if pantheon is None:
		pantheon = random.choice([p for p in PANTHEONS])
	
	god = random.choice([g for g in PANTHEONS[pantheon]["gods"]])
	god_data = PANTHEONS[pantheon]["gods"][god]
	return (god, pantheon, god_data)

if __name__ == "__main__":
	# if search_gods("Anu"):
	# 	Dprint.dp("Function: search_gods() works!")
	# if search_rivals("Tezcat"):
	# 	search_rivals("Tezcat")
	# 	Dprint.dp("Function: search_rivals() works!")
	# if search_pantheon("Pese"):
	# 	Dprint.dp("Function: search_pantheon() works!")
	integrity_check = search_favoured("art")
	if integrity_check:
		Dprint.dp("Function: search_favoured() works!")
		for god in integrity_check:
			Dprint.dp(f"{god['name']} - {god['favoured']['abilities']}")
			Dprint.dp(f"Search results: {len(integrity_check)}")

	# if search_favoured("Perce"):
	# 	Dprint.dp("Function: search_favoured() works!")
	# if search_favoured("Anim"):
	# 	Dprint.dp("Function: search_favoured() works!")
	# if get_virtues("Dodekatheon"):
	# 	Dprint.dp("Function: get_virtues() works!")

	#god, pantheon, god_data = get_random_pantheon_god()
