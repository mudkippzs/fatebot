from datetime import datetime
from pprint import pprint as pp

from player import Player
from player import generate_random_npc
from main import rolldice

from characters import pc_bob 
from characters import pc_vasily 
from characters import pc_jean 
from characters import pc_set 
from characters import pc_set_ferdiad 
from characters import pc_set_standard_summon

from npcs import npc_template

class Battle:
	tick = {
		"0":[],
		"1":[],
		"2":[],
		"3":[],
		"4":[],
		"5":[],
		"6":[],
		"7":[],
		"8":[],
		"9":[],
		"10":[],
		"11":[],
		"12":[],
		"13":[],
		"14":[],
		"15":[],
		"16":[],
		"17":[],
		"18":[],
		"19":[],
		"20":[]
	}

	current_tick = 0
	max_initiative = 6
	players = []

	def __init__(self, players: list=[]):
		if players:
			players = players
			for player in players:
				if player[1] > 6:
					max_initiative = 6
				else:
					max_initiative = player[1]

			print(f"Highest initiative in Player Join Battle rolls: {max_initiative}")
			print(f"Rolling Join Battle for {len(players)} players...")
			self.join_battle()
		else:
			print("No players added to Battle.")

	def join_battle(self):
		for player in players:
			print(player[0], player[1], player[2])
			name = player[0]
			jb = player[1]
			ea = player[2]
			dice_results, successes, extra_successes, success_total = rolldice(f"{jb},0,{ea}")
			print(f"Results for {player}")
			print(f"Dice results:\t{dice_results}")
			print(f"Successes:\t{successes}")
			print(f"Automatic Successes:\t{extra_successes}")
			print(f"Total Successes:\t{success_total}")
			position = self.max_initiative - success_total
			if position <0:
				position = 0
			self.tick[str(position)].append(player)
		print(self.tick)

	def player_action(player, action):
		if action == "melee":
			speed = player.combat["melee"]
		elif action == "range":
			speed = player.combat["range"]
		elif action == "aim":
			speed = player.combat["aim"]
		elif action == "guard":
			speed = player.combat["guard"]
		elif action == "grapple":
			speed = player.combat["grapple"]
		elif action == "inactive":
			speed =player.combat["inactive"]
		

	def add_player(self, player: Player=None):
		if player:
			players.append(player)
		else:
			print(f"Error: expected: 'Player', got: {player}") 

	def next_tick(self):
		self.current_tick += 1
		if self.current_tick > 20:
			self.current_tick = 1

	def __str__(self):
		current_players = ",".join(self.tick[str(self.current_tick)])
		return f"Current tick: {self.current_tick}\nActive players: {current_players}"

if __name__ == "__main__":
	bob_joe = Player("Bob",382348220405383171, False, 3, pc_bob.PLAYER_CHARACTER_SHEET)
	vasily_tom = Player("Vasily Volkov",514859386116767765, False, 3, pc_vasily.PLAYER_CHARACTER_SHEET)
	jean_potato = Player("Jeanne Chadwick",374853432168808448, False, 3, pc_jean.PLAYER_CHARACTER_SHEET)
	set_liddy = Player("Set", 433097995832000513, False, 3, pc_set.PLAYER_CHARACTER_SHEET)
	set_ferdiad = Player("Ferdiad (Set's Summon)", 433097995832000513, False, 3, pc_set_ferdiad.PLAYER_CHARACTER_SHEET)
	set_standard_summon = Player("Fianna Warrior (Set's Summon)", 433097995832000513, False, 3, pc_set_standard_summon.PLAYER_CHARACTER_SHEET)
	
	# Band
	band = [
		bob_joe,
		vasily_tom,
		jean_potato,
		set_liddy,
		set_ferdiad,
		set_standard_summon,
	]

	# NPCs
	npc_list = []
	for _ in range(1, 10):
		npc_list.append(generate_random_npc("Test NPC Grunt", 2))

	pp(npc_list)