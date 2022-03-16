from datetime import datetime
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

from clogger import clogger

from player import Player
from cogs.roller import Roller
from npc import NPC

from npcs import npc_template

import json
import random

import battlemenus


class Battle:

    tick = {
        "0": [],
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": [],
        "9": [],
        "10": [],
        "11": [],
        "12": [],
        "13": [],
        "14": [],
        "15": [],
        "16": [],
        "17": [],
        "18": [],
        "19": [],
        "20": [],
        "21": [],
        "22": [],
        "23": [],
        "24": [],
        "25": []
    }

    current_tick = 0
    max_initiative = 6
    players = []

    def get_max_initiative(self, player):
        max_initiative = 0
        if player.npc[0] is True:
            jb = player.join_battle()
        else:
            jb = player.join_battle

        if jb > 6:
            max_initiative = 6
        else:
            max_initiative = jb

        return max_initiative

    def __init__(self, players: list=[]):
        if len(players):
            for player in players:
                max_initiative = self.get_max_initiative(player)

                self.players = players

                clogger(f"Highest initiative in Player\
                 Join Battle rolls: {max_initiative}")
                clogger(f"Rolling Join Battle for {len(players)} players...")
                self.join_battle()
        else:
            clogger("No players added to Battle.")

    def join_battle(self):
        for player in self.players:
            if player.npc == True:
                name = player.label
            else:
                name = player.name

            if player.npc[0] is True:
                jb = player.join_battle()
            else:
                jb = player.join_battle

            position = self.max_initiative - jb
            if position < 0:
                position = 0

            self.tick[str(position)].append(player)

    async def before_tick(self, battle_context):
        await battle_context.send(self.__str__())
        return

    async def do_tick(self, battle_context, bot):
        done_list = []
        for idx, player in enumerate(self.tick[str(self.current_tick)]):
            clogger(f"PLAYER UP: {player.name}")
            if player.is_dead is False:
                speed = random.randint(1, 5)
                clogger((player.name, player.npc, self.current_tick, speed))
                if player.npc[0]:
                    roll_string = player.get_action_roll(action='unarmed')
                    successes_rolled = await Roller.roll(None,
                                                         battle_context,
                                                         roll_string,
                                                         True,
                                                         None)

                    await battle_context.send(
                        f"```{player.name} rolled - got {successes_rolled} successes```")
                else:
                    mention = f"<@{player.discord_tag}>"
                    interaction_message = await battle_context.send(f"{mention} `Its your turn to act, what do you do?`",
                                                                    components=battlemenus.CHOOSE_ACTION)

                    interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id in ["attack", "shoot", "throw", "aim", "guard", "grapple"] and i.user.id == player.discord_tag)
                    interaction_message = await interaction_message.edit(f"{mention} `choose: {interaction.custom_id}?`",
                                                                         components=battlemenus.CHOOSE_ACTION_2)

                    try:
                        await interaction.respond()
                    except:
                        pass

                    interaction = await bot.wait_for("button_click", check=lambda i: i.custom_id in ["attack", "shoot", "throw", "aim", "guard", "grapple"] and i.user.id == player.discord_tag)
                    await interaction_message.delete()

                    try:
                        await interaction.respond()
                    except:
                        pass

                done_list.append(
                    (self.tick[str(self.current_tick)][idx], speed))

            else:
                dead_player = self.tick[str(self.current_tick)].pop(idx)
                self.graveyard.append(dead_player)
                await battle_context.send(f"```{dead_player.name} \
                    is dead! Sent to Gravyard!```")

        for p in done_list:
            self.tick[str(self.current_tick + p[1])].append(p[0])
        self.tick[self.current_tick] = []

        return

    async def after_tick(self, battle_context):
        pass

    def add_player(self, player: Player = None):
        if player:
            self.players.append(player)
        else:
            print(f"Error: expected: 'Player', got: {player}")

    def next_tick(self):
        self.current_tick += 1
        if self.current_tick > 20:
            self.current_tick = 1

    def __str__(self):
        current_players = ",".join(
            [p.name for p in self.tick[str(self.current_tick)]])
        return f"```Current tick: {self.current_tick}\n" \
            f"Active players: {current_players}```"


if __name__ == "__main__":
    # bob_joe = Player("Bob", 382348220405383171, False,
    #                  3, pc_bob.PLAYER_CHARACTER_SHEET)
    # vasily_tom = Player("Vasily Volkov", 514859386116767765,
    #                     False, 3, pc_vasily.PLAYER_CHARACTER_SHEET)
    # jean_potato = Player("Jeanne Chadwick", 374853432168808448,
    #                      False, 3, pc_jean.PLAYER_CHARACTER_SHEET)
    # set_liddy = Player("Set", 433097995832000513, False,
    #                    3, pc_set.PLAYER_CHARACTER_SHEET)
    # set_ferdiad = Player("Ferdiad (Set's Summon)", 433097995832000513,
    #                      False, 3, pc_set_ferdiad.PLAYER_CHARACTER_SHEET)
    # set_standard_summon = Player("Fianna Warrior (Set's Summon)", 433097995832000513,
    #                              False, 3, pc_set_standard_summon.PLAYER_CHARACTER_SHEET)

    # Band
    # band = [
    #     bob_joe,
    #     vasily_tom,
    #     jean_potato,
    #     set_liddy,
    #     set_ferdiad,
    #     set_standard_summon,
    # ]

    # NPCs
    # npc_list = []
    # for _ in range(0, 5):
    #     print(f"Generating NPC {_+1}...")
    #     n = NPC(label="Grunt", legend=6, debug=True)
    #     n.save_to_dict()
    #     npc_list.append(n.player)

    # all_battlers = band + npc_list

    # b = Battle(all_battlers)
    # b.join_battle()
    # for _ in range(20):
    #     print(b)
    #     b.next_tick()
    pass
