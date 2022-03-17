import discord
from discord.ext import tasks, commands
import json
import os
import random
import sys
import time

from discord_components import DiscordComponents, ComponentsBot, Button

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger

scoreboard_file_name = "scoreboard_test.json"

engaged_list = []


def load_score_board():
    with open(f"{scoreboard_file_name}", "r") as f:
        scoreboard = json.load(f)

    return scoreboard


def save_score_board(scoreboard):
    with open(f"{scoreboard_file_name}", "w") as f:
        json.dump(scoreboard, f)

    return


def get_score(uid, guild_id):
    scoreboard = load_score_board()

    # if user does not exist, add them to the scoreboard
    users = [u["uid"] for u in scoreboard[str(guild_id)]["xo_leaderboard"]]

    if uid not in users:
        scoreboard[str(guild_id)]["xo_leaderboard"].append(
            {"uid": uid, "score": 0})
    # if user exists, update their score if it's higher than their current score
    else:
        for i in range(len(scoreboard[str(guild_id)]["xo_leaderboard"])):
            if scoreboard[str(guild_id)]["xo_leaderboard"][i]["uid"] == uid:
                return scoreboard[str(guild_id)]["xo_leaderboard"][i]["score"]


def process_score(uid, guild_id, score):
    scoreboard = load_score_board()

    # if user does not exist, add them to the scoreboard
    users = [u["uid"] for u in scoreboard[str(guild_id)]["xo_leaderboard"]]

    if uid not in users:
        scoreboard[str(guild_id)]["xo_leaderboard"].append(
            {"uid": uid, "score": score})
    # if user exists, update their score if it's higher than their current score
    else:
        for i in range(len(scoreboard[str(guild_id)]["xo_leaderboard"])):
            if scoreboard[str(guild_id)]["xo_leaderboard"][i]["uid"] == uid:
                if score > scoreboard[str(guild_id)]["xo_leaderboard"][i]["score"]:
                    scoreboard[str(guild_id)
                               ]["xo_leaderboard"][i]["score"] = score

    sorted_scores = sorted(
        scoreboard[str(guild_id)]["xo_leaderboard"], key=lambda k: k['score'], reverse=True)

    scoreboard[str(guild_id)]["xo_leaderboard"] = sorted_scores
    # save the updated leaderboards to file.
    save_score_board(scoreboard)

    return


def position_validator(grid, choice):
    if choice == None:
        return False
    for row in grid:
        for position in row:
            if position.custom_id == choice:
                if position.label != "➖":
                    return False
    return True


def check_engaged(uid):
    for idx, u in enumerate(engaged_list):
        if uid.id == u[0].id or uid == u[1].id:
            return u
    return False


def add_engaged(uid, opponent):
    for idx, u in enumerate(engaged_list):
        if uid.id == u[0].id or uid == u[1].id:
            return False
    engaged_list.append((uid, opponent))
    return True


def remove_engaged(uid):
    for idx, u in enumerate(engaged_list):
        if uid.id == u[0].id or uid == u[1].id:
            _ = engaged_list.pop(idx)
            return True
    return False


def check_winner(position_list):
    print("Checking winner!")
    winning_positions = [
        ["0", "1", "2"],
        ["3", "4", "5"],
        ["6", "7", "8"],
        ["0", "3", "6"],
        ["1", "4", "7"],
        ["2", "5", "8"],
        ["0", "4", "8"],
        ["2", "4", "6"]
    ]

    position_list = sorted(position_list)
    for win_pos in winning_positions:
        if set(win_pos).issubset(position_list):
            return True
    return False


class ExsOhs(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.check_leaderboard.stop()
        self.check_leaderboard.start()

    @commands.command(aliases=["xol", "xoleaderboard"])
    async def xo_leaderboard(self, ctx):
        """Prints the current scoreboard."""

        with open(f"{scoreboard_file_name}", "r") as f:
            data = json.load(f)

        xo_leaderboard = data[str(ctx.guild.id)]["xo_leaderboard"]

        # Sort by score in descending order
        xo_leaderboard = sorted(
            xo_leaderboard, key=lambda x: x["score"], reverse=True)
        if len(xo_leaderboard):
            # Create a list of usernames from uid's
            user_names = []

            for i in range(len(xo_leaderboard)):
                user_names.append(str(xo_leaderboard[i]["uid"]))

            embed = discord.Embed()

            # Set author field of embed to "Leaderboards"
            embed.set_author(name="Middle Ground Xs and Os - Leaderboard")
            medals = ["🏅", "🥇", "🥈", "🥉", "🎖️", "🏆"]
            top_players_header = f"{medals[5]}Top Players{medals[5]}"
            other_players_header = f"{medals[4]}Everyone else{medals[4]}"
            embed.add_field(name="\u200b", value=f"```{top_players_header:^10}```",
                            inline=False)  # name, score

            # 0, 1, 2 (top 3)
            for i in range(len(data[str(ctx.message.guild.id)]["xo_leaderboard"][0:3])):
                user = self.bot.get_user(int(user_names[i]))
                username = user.name
                discriminator = user.discriminator
                if xo_leaderboard[i]['score']:
                    embed.add_field(
                        name="\u200b", value=f"```markdown\n{medals[i + 1]} {username.title():<15}{xo_leaderboard[i]['score']:>5}```", inline=False)  # name, score

            embed.add_field(name="\u200b", value=f"```{other_players_header:^10}```",
                            inline=False)  # name, score

            # 0, 1, 2 (top 3)
            for i in range(len(data[str(ctx.message.guild.id)]["xo_leaderboard"][4:])):
                user = self.bot.get_user(int(user_names[i + 4])).display_name
                embed.add_field(
                    name="\u200b", value=f"```markdown\n{medals[0]}. {username:<15}{xo_leaderboard[i + 4]['score']:>5}```", inline=False)  # name, score

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"```There is no scores logged yet. Type ?xo to start a new game!```")

    @commands.command(aliases=["ox", "oxs", "ohexs", "ohex", "exsohs", "noughtsandcrosses", "naughtsandcrosses", "xos", "exoh"])
    async def xo(self, ctx, opponent: discord.Member = None):
        if opponent == None:
            opponent = self.bot.user

        engaged_check = check_engaged(ctx.author)
        opponent_engaged_check = check_engaged(opponent.id)
        
        if opponent_engaged_check is True:
            ctx.send(
                f"```{opponent.display_name} is already playing: {opponent.display_name} vs {opponent_engaged_check[1]}```")
            return

        if engaged_check is False:
            welcome_message = "Welcome to the Middle Ground X's and O's Game!"
            opening_message = "Naughts and Crosses, Ex's and Oh's, Noughts? and Crosses! Whatever you call it, play it here with a buddy or play against the bot!"

            add_engaged(ctx.author, opponent)
            add_engaged(opponent, ctx.author)

            task_message = "\n\n# How it works!\n\n* Take turns choosing positions to place symbols!\n* Make a line (diagonally or laterally) of 3 symbols!\n* Win!"
            player_symbol_choices = ["✖️", "⭕"]
            empty_symbol = "➖"
            player_symbols = [None, None]

            intro_title = await ctx.send(f"```{welcome_message:<40}```")
            intro_message = await ctx.send(f"```markdown\n{opening_message:<50}{task_message:<50}```")
            interaction_message = await ctx.send(f"```Ready?```", components=[
                [
                    Button(label=f"I'll be {player_symbol_choices[0]}",
                           custom_id="0", style=2),
                    Button(label=f"I'll be {player_symbol_choices[1]}",
                           custom_id="1", style=2),
                    Button(label=f"I don't want to play right now!",
                           custom_id="cancel_1", style=3)
                ]
            ])

            interaction = await self.bot.wait_for("button_click", check=lambda i: i.custom_id in ["0", "1", "cancel_1"] and i.user.id == ctx.author.id)

            player_symbols[1] = player_symbol_choices.pop(int(interaction.custom_id))
            player_symbols[0] = player_symbol_choices[0]
            

            if interaction.custom_id == "cancel_1":
                await ctx.send(f"```Ok, come back any time!```", delete_after=5.0)
                await interaction_message.delete()
                await ctx.message.delete()
                await intro_title.delete()
                await intro_message.delete()
                remove_engaged(ctx.author)
                remove_engaged(opponent)
                return

            try:
                await interaction.respond(type=6)
            except:
                pass

            if opponent.bot is False:
                interaction_message = await ctx.send(f"```OK! {opponent}! Are you ready?```",
                                                     components=[
                                                         [
                                                             Button(label="I'm ready!!",
                                                                    custom_id="ready", style=1),
                                                             Button(
                                                                 label="I don't want to play right now!", custom_id="cancel_2", style=3)
                                                         ]
                                                     ])

                interaction = await self.bot.wait_for("button_click", check=lambda i: i.custom_id in ["ready", "cancel_2"] and i.user.id == opponent.id)

                if interaction.custom_id == "cancel_2":
                    await ctx.send(f"```Ok, come back any time!```", delete_after=5.0)
                    await interaction_message.delete()
                    await ctx.message.delete()
                    await intro_title.delete()
                    await intro_message.delete()
                    remove_engaged(ctx.author)
                    remove_engaged(opponent)
                    return

            player_postitions = [
                [],  # player 1's moves.
                []  # player 2's moves.
            ]

            player_list = [ctx.message.author, opponent]

            random.shuffle(player_list)
            current_player = 0
            grid_positions = [
                [
                    Button(label=f"{empty_symbol}", custom_id="0",
                           style=2),
                    Button(label=f"{empty_symbol}", custom_id="1",
                           style=2),
                    Button(label=f"{empty_symbol}", custom_id="2",
                           style=2),
                ],
                [
                    Button(label=f"{empty_symbol}", custom_id="3",
                           style=2),
                    Button(label=f"{empty_symbol}", custom_id="4",
                           style=2),
                    Button(label=f"{empty_symbol}", custom_id="5",
                           style=2),
                ],
                [
                    Button(label=f"{empty_symbol}", custom_id="6",
                           style=2),
                    Button(label=f"{empty_symbol}", custom_id="7",
                           style=2),
                    Button(label=f"{empty_symbol}", custom_id="8",
                           style=2),
                ]
            ]

            while True:

                if player_list[current_player].bot is False:
                    await interaction_message.edit(f"```Choose a position...```")

                    choice = None
                    while position_validator(grid_positions, choice) != True:
                        game_interaction_message = await interaction_message.edit(f"```...```", components=grid_positions)
                        game_interaction = await self.bot.wait_for("button_click", check=lambda i: i.user.id == player_list[current_player].id)

                        try:
                            await game_interaction.respond(type=6)
                        except Exception as e:
                            pass

                        choice = game_interaction.custom_id

                    player_postitions[current_player].append(str(choice))

                else:
                    possible_choices = [c for c in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
                                        if c not in player_postitions[current_player] and c not in player_postitions[current_player - 1]]
                    if len(possible_choices) == 0:
                        winner = None
                        loser = None
                        break
                    random.shuffle(possible_choices)
                    choice = str(random.choice(possible_choices))
                    player_postitions[current_player].append(str(choice))

                for row in grid_positions:
                    for grid_pos in row:
                        if grid_pos.custom_id == str(choice):
                            grid_pos.label = player_symbols[int(
                                current_player)]

                if check_winner(player_postitions[current_player]):
                    winner = player_list[current_player]
                    loser = player_list[current_player - 1]
                    time.sleep(2)
                    break
                else:
                    if current_player == 1:
                        current_player = 0
                    elif current_player == 0:
                        current_player = 1

            if winner is not None:
                if winner.bot is False:
                    score_msg = await ctx.send(f"🏆 {winner.mention} won! 🏆 Better luck next time {loser.mention}!\n\n```Type ?xo to play again, @someone or play against the bot!```")
                    score = get_score(winner.id, ctx.message.guild.id)
                    if score is None:
                        score = 1
                    else:
                        score += 1

                    process_score(uid=winner.id, score=score,
                                  guild_id=ctx.message.guild.id)
            else:
                score_msg = await ctx.send(f"🥴 Draw! Better luck next time!\n\n```Type ?xo to play again, @someone or play against the bot!```")

            # await intro_title.delete()
            # await intro_message.delete()
            await self.xo_leaderboard(ctx)
            remove_engaged(ctx.author)
            remove_engaged(opponent)

        else:
            author_name = ctx.message.author.display_name
            opponent_name = opponent.display_name
            await ctx.send(f"`You are already playing: {author_name} vs {opponent_name} in {ctx.message.channel.name}!`\n``` You can't play multiple people at the same time.```", delete_after=5.0)

        remove_engaged(ctx.author)
        remove_engaged(opponent)

    @tasks.loop(seconds=15)
    async def check_leaderboard(self):
        #clogger("Updating PB Leaderboard.")
        guild_whitelist = [820077049036406805, 832999632028041226]
        for guild in self.bot.guilds:
            if guild.id in guild_whitelist:
                with open(f'{scoreboard_file_name}', 'r') as f:
                    data = json.load(f)
                xo_leaderboard = data[str(guild.id)]['xo_leaderboard']
                with open('roles.json', 'r') as f:
                    data = json.load(f)
                roles = data['roles'][1]

                for i in range(len(xo_leaderboard)):
                    index = i

                    # Assign the Roles to the users in first, second and third place respectively
                    if index == 0:
                        # Gold Role ID: 707926590981440779
                        role = discord.utils.get(guild.roles, name=roles[0])
                    elif index == 1:
                        # Silver Role ID: 707926590981440781
                        role = discord.utils.get(guild.roles, name=roles[1])
                    elif index == 2:
                        # Bronze Role ID: 707926590981440781
                        role = discord.utils.get(guild.roles, name=roles[2])
                    else:
                        # Contender Role ID: 707926590981440781
                        role = discord.utils.get(guild.roles, name=roles[3])

                    uid = int(xo_leaderboard[index]['uid'])
                    userobj = guild.get_member(uid)
                    await guild.get_member(uid).add_roles([role], f"Achieved `{roles[i]}` in MG XOs Game.", atomic=True)


def setup(client):
    client.add_cog(ExsOhs(client))
