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


def load_score_board():
    with open("scoreboard.json", "r") as f:
        scoreboard = json.load(f)

    return scoreboard


def save_score_board(scoreboard):
    with open("scoreboard.json", "w") as f:
        json.dump(scoreboard, f)

    return


def process_score(uid, score):
    scoreboard = load_score_board()

    # if user does not exist, add them to the scoreboard
    users = [u["uid"] for u in scoreboard["xo_leaderboard"]]

    if uid not in users:
        scoreboard["xo_leaderboard"].append({"uid": uid, "score": score})
    # if user exists, update their score if it's higher than their current score
    else:
        for i in range(len(scoreboard["xo_leaderboard"])):
            if scoreboard["xo_leaderboard"][i]["uid"] == uid:
                if score > scoreboard["xo_leaderboard"][i]["score"]:
                    scoreboard["xo_leaderboard"][i]["score"] = score

    sorted_scores = sorted(
        scoreboard["xo_leaderboard"], key=lambda k: k['score'], reverse=True)

    # save the updated leaderboards to file.
    save_score_board({"xo_leaderboard": sorted_scores})

    return


class ExsOhs(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.check_leaderboard.stop()
        self.check_leaderboard.start()

    @commands.command(aliases=["xol", "xoleaderboard"])
    async def xo_leaderboard(self, ctx):
        """Prints the current scoreboard."""

        with open("scoreboard.json", "r") as f:
            data = json.load(f)

        xo_leaderboard = data["xo_leaderboard"]

        # Sort by score in descending order
        xo_leaderboard = sorted(
            xo_leaderboard, key=lambda x: x["score"], reverse=True)

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

        for i in range(len(data["xo_leaderboard"][0:3])):  # 0, 1, 2 (top 3)
            user = self.bot.get_user(int(user_names[i]))
            username = user.name
            discriminator = user.discriminator

            embed.add_field(
                name="\u200b", value=f"```markdown\n{medals[i + 1]} {username.title():<15}{xo_leaderboard[i]['score']:>5}```", inline=False)  # name, score

        embed.add_field(name="\u200b", value=f"```{other_players_header:^10}```",
                        inline=False)  # name, score

        for i in range(len(data["xo_leaderboard"][4:])):  # 0, 1, 2 (top 3)
            user = self.bot.get_user(int(user_names[i + 4])).display_name
            embed.add_field(
                name="\u200b", value=f"```markdown\n{medals[0]}. {username:<15}{xo_leaderboard[i + 4]['score']:>5}```", inline=False)  # name, score

        await ctx.send(embed=embed)

    @commands.command(aliases=["exsohs", "noughtsandcrosses", "naughtsandcrosses", "xos", "exoh"])
    async def xo(self, ctx, opponent: discord.Member = None):
        welcome_message = "Welcome to the Middle Ground X's and O's Game!"
        opening_message = "Naughts and Crosses, Ex's and Oh's, Noughts? and Crosses! Whatever you call it, play it here with a buddy or play against the bot!"
        task_message = "\n\n# How it works!\n\n* Take turns choosing positions to place symbols!\n* Make a line (diagonally or laterally) of 3 symbols!\n* Win!"

        intro_title = await ctx.send(f"```{welcome_message:<40}```")
        intro_message = await ctx.send(f"```markdown\n{opening_message:<50}{task_message:<50}```")
        interaction_message = await ctx.send(f"```Ready?```", components=[
            [
                Button(label=f"I'll be {x_symbol}!",
                       custom_id="ready", style=1),
                Button(label=f"I'll be {y_symbol}", custom_id="cancel", style=1),                
                Button(label=f"I don't want to play right now!", custom_id="cancel", style=3)
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
            await interaction.respond()
        except:
            pass

        await interaction_message.delete()
        interaction_message = await ctx.send(f"```OK! {opponent}! Are you ready?```",
                                             components=[
                                                 [
                                                     Button(label="I'm ready!!",
                                                            custom_id="ready", style=1),
                                                     Button(
                                                         label="I don't want to play right now!", custom_id="cancel", style=3)
                                                 ]
                                             ])

        interaction = await self.bot.wait_for("button_click", check=lambda i: i.custom_id in ["ready", "cancel"] and i.user.id == opponent.id)

        if interaction.custom_id != "ready":
            await ctx.send(f"```Ok, come back any time!```", delete_after=5.0)
            await interaction_message.delete()
            await ctx.message.delete()
            await intro_title.delete()
            await intro_message.delete()
            return

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
                await game_interaction.respond()
            except:
                pass

            score += 1

        await interaction_message.delete()
        score_msg = await ctx.send(f"```{ctx.author.display_name}'s score: {score}```")
        process_score(uid=ctx.author.id, score=score)
        await intro_title.delete()
        await intro_message.delete()
        await score_msg.delete()
        await self.paddleboard_leaderboard(ctx)

    @tasks.loop(seconds=15)
    async def check_leaderboard(self):
        #clogger("Updating PB Leaderboard.")
        guild_whitelist = [820077049036406805, ]
        for guild in self.bot.guilds:
            if guild.id in guild_whitelist:
                with open('scoreboard.json', 'r') as f:
                    data = json.load(f)
                xo_leaderboard = data['xo_leaderboard']
                with open('roles.json', 'r') as f:
                    data = json.load(f)
                roles = data['roles']

                for i in range(len(xo_leaderboard)):
                    index = i

                    # Assign the Roles to the users in first, second and third place respectively
                    if index == 0:
                        # Gold Role ID: 707926590981440779
                        role = discord.utils.get(guild.roles, name=roles[1][0])
                    elif index == 1:
                        # Silver Role ID: 707926590981440781
                        role = discord.utils.get(guild.roles, name=roles[1][1])
                    elif index == 2:
                        # Bronze Role ID: 707926590981440781
                        role = discord.utils.get(guild.roles, name=roles[1][2])
                    else:
                        # Contender Role ID: 707926590981440781
                        role = discord.utils.get(guild.roles, name=roles[1][3])

                    uid = int(xo_leaderboard[index]['uid'])
                    userobj = guild.get_member(uid)
                    await guild.get_member(uid).add_roles([role], f"Achieved `{role.name}` in MG PB Game.", atomic=True)


def setup(client):
    client.add_cog(ExsOhs(client))
