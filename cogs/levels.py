"""
1. Create a discord cog for levels.
2. Map levels to roles by ID in a JSON file.
3. Create a custom image for user levels.
4. Create a user ID embded with user info, level and roles.
"""

import discord
from discord.ext import commands
import json
import os
import random
import sys
import asyncio
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger

def calculate_xp(message_text, current_level):
    message_size = len(message_text.replace(" ", ""))

    if message_size > 30:
        xp = message_size * (current_level * 0.5)/100
    else:
        xp = random.randint(0,5)

    return xp 


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if "text" in message.channel.type:
            if "log" not in message.channel.name:
                if message.author == self.bot.user:
                    return

                with open("levels.json", "r") as f:
                    users = json.load(f)

                if not str(message.guild.id) in users:
                    users[str(message.guild.id)] = {}

                if not str(message.author.id) in users[str(message.guild.id)]:
                    users[str(message.guild.id)][str(message.author.id)] = {}
                    users[str(message.guild.id)][str(
                        message.author.id)]["experience"] = 0
                    users[str(message.guild.id)][str(
                        message.author.id)]["level"] = 1

                users[str(message.guild.id)][str(message.author.id)]["experience"] += calculate_xp(
                    message.clean_content,
                    users[str(message.guild.id)][str(message.author.id)]["level"])

                with open("levels.json", "w") as f:
                    json.dump(users, f, indent=4)

                def check_level(user):
                    if user["experience"] >= user["level"] * 10:
                        return True
                    else:
                        return False

                if check_level(users[str(message.guild.id)][str(message.author.id)]):
                    users[str(message.guild.id)][str(
                        message.author.id)]["experience"] = 0
                    users[str(message.guild.id)][str(
                        message.author.id)]["level"] += 1

                    with open("levels.json", "w") as f:
                        json.dump(users, f, indent=4)

                    #await message.channel.send(f"{message.author} has leveled up to level {users[str(message.guild.id)][str(message.author.id)]['level']}!")

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        with open("levels.json", "r") as f:
            users = json.load(f)

        if not str(ctx.guild.id) in users:
            users[str(ctx.guild.id)] = {}

        if not str(member.id) in users[str(ctx.guild.id)]:
            users[str(ctx.guild.id)][str(member.id)] = {}
            users[str(ctx.guild.id)][str(member.id)]["experience"] = 0
            users[str(ctx.guild.id)][str(member.id)]["level"] = 1

        embed = discord.Embed(
            title=f"{member}'s level", description=f"Level {users[str(ctx.guild.id)][str(member.id)]['level']}", color=0x00ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Experience", value=users[str(
            ctx.guild.id)][str(member.id)]["experience"])
        await ctx.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        with open("levels.json", "r") as f:
            users = json.load(f)

        if not str(ctx.guild.id) in users:
            users[str(ctx.guild.id)] = {}

        leaderboard_title = "MG Leaderboard"
        embed = discord.Embed(title=f"{leaderboard_title:<32}", color=0x00ff00)
        #embed.set_thumbnail(url=ctx.guild.icon_url)

        sorted_users = sorted(users[str(ctx.guild.id)].items(
        ), key=lambda x: x[1]["level"], reverse=True)

        member_string = "Member"
        level_string = "Level"
        
        embed.add_field(
            name=f"\u200b", value=f"{member_string:<50}", inline=True)
        embed.add_field(
            name=f"\u200b", value=f"{level_string:>50}", inline=True)
        
        for idx, user in enumerate(sorted_users[:10]):
            member = ctx.guild.get_member(int(user[0]))
            level_string = f"{user[1]['level']}"
            embed.add_field(
                name=f"\u200b", value=f"```{idx + 1}. {member}{level_string:>22}```", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        with open("levels.json", "r") as f:
            users = json.load(f)

        if not str(ctx.guild.id) in users:
            users[str(ctx.guild.id)] = {}

        if not str(member.id) in users[str(ctx.guild.id)]:
            users[str(ctx.guild.id)][str(member.id)] = {}
            users[str(ctx.guild.id)][str(member.id)]["experience"] = 0
            users[str(ctx.guild.id)][str(member.id)]["level"] = 1

        sorted_users = sorted(users[str(ctx.guild.id)].items(
        ), key=lambda x: x[1]["level"], reverse=True)

        for i, user in enumerate(sorted_users):
            if int(user[0]) == member.id:
                break

        embed = discord.Embed(
            title=f"{member}'s rank", description=f"Rank {i + 1}", color=0x00ff00)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        with open("levels.json", "r") as f:
            users = json.load(f)

        if not str(ctx.guild.id) in users:
            users[str(ctx.guild.id)] = {}

        if not str(member.id) in users[str(ctx.guild.id)]:
            users[str(ctx.guild.id)][str(member.id)] = {}
            users[str(ctx.guild.id)][str(member.id)]["experience"] = 0
            users[str(ctx.guild.id)][str(member.id)]["level"] = 1

        sorted_users = sorted(users[str(ctx.guild.id)].items(
        ), key=lambda x: x[1]["level"], reverse=True)

        for i, user in enumerate(sorted_users):
            if int(user[0]) == member.id:
                break

        embed = discord.Embed(title=f"{member}'s profile", color=0x00ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Level", value=users[str(
            ctx.guild.id)][str(member.id)]["level"])
        embed.add_field(name="Experience", value=users[str(
            ctx.guild.id)][str(member.id)]["experience"])
        embed.add_field(name="Rank", value=i + 1)
        await ctx.send(embed=embed)

    @commands.command()
    async def levelimage(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        with open("levels.json", "r") as f:
            users = json.load(f)

        if not str(ctx.guild.id) in users:
            users[str(ctx.guild.id)] = {}

        if not str(member.id) in users[str(ctx.guild.id)]:
            users[str(ctx.guild.id)][str(member.id)] = {}
            users[str(ctx.guild.id)][str(member.id)]["experience"] = 0
            users[str(ctx.guild.id)][str(member.id)]["level"] = 1

        sorted_users = sorted(users[str(ctx.guild.id)].items(
        ), key=lambda x: x[1]["level"], reverse=True)

        for i, user in enumerate(sorted_users):
            if int(user[0]) == member.id:
                break

        async with aiohttp.ClientSession() as session:
            async with session.get(member.avatar_url) as resp:
                avatar = await resp.read()

        font = ImageFont.truetype("arial.ttf", size=45)
        font2 = ImageFont.truetype("arial.ttf", size=60)

        img = Image.open("level.png").convert("RGBA")
        avatar = Image.open(io.BytesIO(avatar)).resize(
            (170, 170)).convert("RGBA")

        img_w, img_h = img.size
        offset = (170 // 2, 170 // 2)

        img.paste(avatar, offset, avatar)

        draw = ImageDraw.Draw(img)
        draw.text((250, 40), f"{member}", font=font2, fill=(255, 255, 255))
        draw.text((250, 110), f"Level {users[str(ctx.guild.id)][str(member.id)]['level']}", font=font2, fill=(
            255, 255, 255))
        draw.text((250, 180), f"Rank {i + 1}",
                  font=font2, fill=(255, 255, 255))
        draw.text((250, 250), f"Experience {users[str(ctx.guild.id)][str(member.id)]['experience']}", font=font2, fill=(
            255, 255, 255))

        img.save("level_image.png")

        await ctx.send(file=discord.File("level_image.png"))


def setup(bot):
    bot.add_cog(Levels(bot))
