import discord
from discord.ext import tasks, commands
import json
import os
import random
import sys

from discord_components import DiscordComponents, ComponentsBot, Button

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger

scoreboard_file_name = "scoreboard.json"

def load_score_board():
    with open(scoreboard_file_name, "r") as f:
        scoreboard = json.load(f)

    return scoreboard


def save_score_board(scoreboard):
    with open(scoreboard_file_name, "w") as f:
        json.dump(scoreboard, f)

    return


def process_score(uid, guild_id, score):
    scoreboard = load_score_board()

    # if user does not exist, add them to the scoreboard
    users = [u["uid"] for u in scoreboard[str(guild_id)]["pb_leaderboard"]]

    if uid not in users:
        scoreboard["pb_leaderboard"].append({"uid": uid, "score": score})
    # if user exists, update their score if it's higher than their current score
    else:
        for i in range(len(scoreboard["pb_leaderboard"])):
            if scoreboard[str(guild_id)]["pb_leaderboard"][i]["uid"] == uid:
                if score > scoreboard[str(guild_id)]["pb_leaderboard"][i]["score"]:
                    scoreboard[str(guild_id)]["pb_leaderboard"][i]["score"] = score

    sorted_scores = sorted(
        scoreboard[str(guild_id)]["pb_leaderboard"], key=lambda k: k['score'], reverse=True)

    scoreboard[str(guild_id)]["pb_leaderboard"] = sorted_scores
    # save the updated leaderboards to file.
    save_score_board(scoreboard)

    return


class ClickMe(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["pbl"])
    async def paddleboard_leaderboard(self, ctx):
        """Prints the current scoreboard."""

        with open(scoreboard_file_name, "r") as f:
            data = json.load(f)

        pb_leaderboard = data[str(ctx.guild.id)]["pb_leaderboard"]

        # Sort by score in descending order
        pb_leaderboard = sorted(
            pb_leaderboard, key=lambda x: x["score"], reverse=True)

        if len(pb_leaderboard):
            # Create a list of usernames from uid's
            user_names = []

            for i in range(len(pb_leaderboard)):
                user_names.append(str(pb_leaderboard[i]["uid"]))

            embed = discord.Embed()

            # Set author field of embed to "Leaderboards"
            embed.set_author(
                name="MG Paddleball Tourney - Leaderboard")
            medals = ["🏅", "🥇", "🥈", "🥉", "🎖️", "🏆"]
            top_players_header = f"{medals[5]}Top Players{medals[5]}"
            other_players_header = f"{medals[4]}Everyone else{medals[4]}"
            embed.add_field(name="\u200b", value=f"```{top_players_header:^30}```",
                            inline=False)  # name, score

            # 0, 1, 2 (top 3)
            for i in range(len(data[str(ctx.guild.id)]["pb_leaderboard"][0:3])):
                user = self.bot.get_user(int(user_names[i]))
                username = user.name
                discriminator = user.discriminator

                embed.add_field(
                    name="\u200b", value=f"```markdown\n{medals[i + 1]} {username.title():<15}{pb_leaderboard[i]['score']:>15}```", inline=False)  # name, score

            embed.add_field(name="\u200b", value=f"```{other_players_header:^32}```",
                            inline=False)  # name, score

            # 0, 1, 2 (top 3)
            for j in range(len(data[str(ctx.guild.id)]["pb_leaderboard"][4:])):
                user = self.bot.get_user(int(user_names[j + 4])).name
                embed.add_field(
                    name="\u200b", value=f"```markdown\n{medals[0]} {user:<15}{pb_leaderboard[j + 4]['score']:>12}```", inline=False)  # name, score

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"```There is no scores logged yet. Type ?xo to start a new game!```")

    @commands.command(aliases=["pb"])
    async def paddleboard(self, ctx):
        welcome_message = "Welcome to the Middle Ground Paddle Tourney!"
        opening_message = "Many a newfag have joined when faced with the wall of deadening silence in chat!\n\nSo I hope this game provides enough wholesome pot-stiring, a fly-wheel for social engagement!"
        task_message = "\n\n# How it works!\n\n* Paddle the ball!\n* Don't miss!\n* ????\n* Profit!"

        intro_title = await ctx.send(f"```{welcome_message:<40}```")
        intro_message = await ctx.send(f"```markdown\n{opening_message:<50}{task_message:<50}```")
        interaction_message = await ctx.send(f"```Ready?```", components=[
            [
                Button(label="I'm ready!", custom_id="ready", style=1),
                Button(label="I'm not ready...", custom_id="cancel", style=3)
            ]
        ])

        interaction = await self.bot.wait_for("button_click", check=lambda i: i.custom_id in ["ready", "cancel"] and i.user.id == ctx.author.id)

        if interaction.custom_id != "ready":
            await ctx.send(f"```Ok, come back any time!```", delete_after=5.0)
            await interaction_message.delete()
            await ctx.message.delete()
            await intro_title.delete()
            await intro_message.delete()
            return

        try:
            await interaction.respond(type=6)
        except:
            pass

        game_interaction_message = await interaction_message.edit(f"```OK! READY? PADDLE THAT BALL!```")
        score = 0
        while True:
            game_text = random.choice(
                ["Click the Ball!", "Get it!", "Dont miss!", "Keep it up!", "Good luck!"])

            ball_emoji = "⚪"
            paddle_emoji = "🏓"

            random_paddle_style = [4, 3, 4]

            random.shuffle(random_paddle_style)
            random.shuffle(random_paddle_style)

            paddle_ball_positions = [
                [
                    Button(label=f"{ball_emoji}", custom_id="ball",
                           style=random_paddle_style[0]),
                    Button(label=f"{paddle_emoji}", custom_id="empty_1",
                           style=random_paddle_style[1]),
                    Button(label=f"{paddle_emoji}", custom_id="empty_2",
                           style=random_paddle_style[2]),
                ]
            ]

            random.shuffle(paddle_ball_positions[0])
            random.shuffle(paddle_ball_positions[0])

            game_interaction_message = await interaction_message.edit(f"```{game_text}```", components=paddle_ball_positions)
            game_interaction = await self.bot.wait_for("button_click", check=lambda i: i.custom_id in ["ball", "empty_1", "empty_2"] and i.user.id == ctx.author.id)

            if game_interaction.custom_id != "ball":
                break

            try:
                await game_interaction.respond(type=6)
            except:
                pass

            score += 1

        await interaction_message.delete()
        score_msg = await ctx.send(f"```{ctx.author.display_name}'s score: {score}```")
        process_score(uid=ctx.author.id, guild_id=ctx.message.guild.id, score=score)

        await intro_title.delete()
        await intro_message.delete()
        await score_msg.delete()
        await self.paddleboard_leaderboard(ctx)
        await self.check_leaderboard()

    async def check_leaderboard(self):
        #clogger("Updating PB Leaderboard.")
        guild_whitelist = [820077049036406805, ]
        for guild in self.bot.guilds:
            if guild.id in guild_whitelist:
                with open('scoreboard.json', 'r') as f:
                    data = json.load(f)
                pb_leaderboard = data[str(guild.id)]['pb_leaderboard']
                with open('roles.json', 'r') as f:
                    data = json.load(f)
                roles = data['roles'][0]

                medal_roles = [discord.utils.get(
                    guild.roles, name=roles[r]) for r in range(0, 3)]

                for i in range(len(pb_leaderboard)):
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

                    uid = int(pb_leaderboard[index]['uid'])
                    userobj = guild.get_member(uid)
                    for medal in medal_roles:
                        await guild.get_member(uid).remove_roles([medal], atomic=True)
                    await guild.get_member(uid).add_roles([role], f"Achieved `{role.name}` in MG XOs Game.", atomic=True)


def setup(client):
    client.add_cog(ClickMe(client))
