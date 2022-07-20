"""
1. Create a discord bot cog that should generate a random number between 1 and 100 at midnight (GMT+1).
3. If the result is 88, 100, 1, 72, 46, 69 then: disable 'change nickname' server permission; for users with 'members' role, and then randomly swap nicknames of all members.
4. No two members should have the same nickname, and no member should have their own nickname and the swap should be random.
5. Send all output to the 📢announcements📢 channel and send the gif: https://c.tenor.com/BU7jcFyIrPoAAAAC/futurama-change-places.gif and @everyone.
6. Reverse the nickname swap after 24 hours.
7. Include a command to trigger this manually instead of waiting for the timer.
"""
import random
from datetime import timedelta, datetime
from discord.ext import commands
from discord import utils, Permissions
import discord
import asyncio
import re
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

import timeago

from clogger import clogger

with open("config.json", "r") as f:
    config = json.load(f)

class ChangePlaces(commands.Cog):
    """Swaps nicknames of all members for 24hrs - 5% chance every day"""
    def __init__(self, client):
        self.client = client
        self.random_swap_members_task = self.client.loop.create_task(self.random_swap_members())

    def cog_unload(self):
        self.random_swap_members_task.cancel()

    @staticmethod
    def random_number():
        return random.randint(1, 100)

    async def random_swap_members(self):
        """Swaps members every day at midnight GMT+1"""
        await self.client.wait_until_ready()  # Wait until the bot has started up properly
        days = 0  # Stores how many days have past since last swap for use in channel message
        channel = utils.find(lambda c: c.name == "📢announcements📢", self.client.get_all_channels())
        while not self.client.is_closed():
            # Wait until we at or past midnight GMT+1
            await self.client.wait_until_gte(datetime.utcnow() + timedelta(hours=1))
            # Get the previous midnight as utc datetime and add 1 day to it
            midnight = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            while datetime.utcnow() < midnight:  # While the current utc time is less than midnight...
                random_number = self.random_number()
                if random_number in (1, 72, 88, 100):  # Check for special numbers
                    guild = self.client.get_guild(self.client.espb_guild_id)  # Get guild from id
                    # Get "Members" role from guild and format into list of role objects
                    member_roles = [role for role in guild.roles if role.name == "Members"]

                    nicknames = {}  # Dict to hold member id's as keys and nicknames as values
                    for member in guild.members:  # Go through every member in the guild...
                        if member_roles[0] in member.roles:  # If they have the "Members" role...
                            if member != guild.owner:  # If they are not the owner...
                                nicknames[member.id] = member.display_name  # Add their nickname to the dict

                    perms = Permissions()  # Create a permissions object and remove the change nickname permission
                    perms.update(change_nickname=False)

                    for role in guild.roles:  # Go through every role in the server...
                        if role == member_roles[0]:  # If we find the members role...
                            await role.edit(permissions=perms)  # Edit that role with removed permissions

                    nicknames = list(nicknames)  # Turn our dict into a list of dict keys

                    while len(nicknames) > 0:  # While we still have members in our list...

                        random1 = random.randint(0, len(nicknames)-1)  # Pick two random numbers between 0 and length-1...
                        random2 = random.randint(0, len(nicknames)-1)

                        temp = nicknames[random1]  # Switch members at those positions in our list

                        member1 = utils.get(guild.members, id=nicknames[random2])  # Get members from member id's
                        member2 = utils.get(guild.members, id=temp)

                        nicknames[random1] = nicknames[random2]

                        await member1.edit(nick=member2.display_name)  # Change their nicknames to each other's names
                        await member2.edit(nick=member1.display_name)

                        del nicknames[random2]  # Remove our list entry so we don't collide with this user again

                    days += 1  # Increment how many days have passed since last swap (for use in message later)

                embed=discord.Embed(title="CHANGE PLACES!", description="For the next 24hrs all members nicknames have been swapped!")
                embed.set_image(url="attachment://futurama-change-places.gif")

                #and send the damn thing
                await channel.send(content="@here", embed=embed, file=discord.File("imgs/futurama-change-places.gif"))

                await self._sleep()    # Sleep until tomorrow is closer than today (which is now yesterday? lol!)

    async def _sleep(self):     
        """Sleeps until tomorrow is nearer than today!"""
        today = datetime.utcnow() + timedelta(hours=1)         # Adds 1 hour because I'm GMT+1, be careful with that!
        midnight = today.replace(hour=0, minute=0, second=0)   # Gets midnight for the current day in utc
        if midnight - datetime.utcnow() >= timedelta(seconds=2):  # If the time between now and midnight is greater than 2 seconds...
            await self.client.wait_until_gte(midnight)           # Wait until we are 24 hours past midnight
        else:
            while (midnight - datetime.utcnow()) < timedelta(seconds=2):   # If it is less than two seconds...
                midnight = midnight + timedelta(days=1)  # Add a day to midnight
            await self.client.wait_until_gte(midnight)  # Wait until midnight or after

    @commands.command()
    async def swap(self, context):
        """Swaps nicknames manually"""
        guild = context.guild
        
        if str(context.message.author.id) in [config["gamemaster"][0]["ganj"]]:  # Checks if owner using command

            member_roles = [role for role in guild.roles if role.name == "Member"]

            for member in guild.members:  # Go through every member in the guild...
                member_roles[0] in member.roles and member != guild.owner  # If they have the "Members" role and aren't the owner...

            perms = Permissions()  # Create a permissions object and remove the change nickname permission
            perms.update(change_nickname=False)

            for role in guild.roles:  # Go through every role in the server...
                if role == member_roles[0]:  # If we find the members role...
                    clogger(f"Role: {role}")
                    clogger(f"Perms: {perms}")
                    await role.edit(permissions=perms)  # Edit that role with removed permissions

            nicknames = {}  # Dict to hold member id's as keys and nicknames as values
            for member in guild.members:  # Go through every member in the guild...
                if member_roles[0] in member.roles:  # If they have the "Members" role...
                    if member != guild.owner and member.bot is False:  # If they are not the owner...
                        nicknames[member.id] = member.display_name  # Add their nickname to the dict

            nicknames = list(nicknames)  # Turn our dict into a list of dict keys

            while len(nicknames) > 1:  # While we still have members in our list...

                random1 = random.choice(nicknames)
                nicknames.remove(random1)                
                random2 = random.choice(nicknames)
                nicknames.remove(random2)

                member1 = utils.get(guild.members, id=random1)     # Get members from their id's from our dict keys/list items
                member2 = utils.get(guild.members, id=random2)
                member_1_new_nick = member2.display_name
                member_2_new_nick = member1.display_name
                await member1.edit(nick=member_1_new_nick)      # Change their nicknames to each other's names! omg crazy! lol! xD :D :) :P ;P ;D ;D ;D <3 :heart: :smile: :sad: :crying: :angry: :stupid: :wut:
                await member2.edit(nick=member_2_new_nick)

            channel = utils.find(lambda c: c.name == "📢announcements📢", self.client.get_all_channels())      
            
            embed=discord.Embed(title="CHANGE PLACES!", description="For the next 24hrs all members nicknames have been swapped!")
            embed.set_image(url="attachment://futurama-change-places.gif")

            #and send the damn thing
            await channel.send(content="@here", embed=embed, file=discord.File("imgs/futurama-change-places.gif"))

        else:
            await context.send("```You must not be a faggot to execute this command```", delete_after=5)

    @commands.command()
    async def changeplacesping(self, context):
        channel = utils.find(lambda c: c.name == "📢announcements📢", self.client.get_all_channels())
        
        embed=discord.Embed(title="CHANGE PLACES!", description="For the next 24hrs all members nicknames have been swapped!")
        embed.set_image(url="attachment://futurama-change-places.gif")

        #and send the damn thing
        await channel.send(content="@here", embed=embed, file=discord.File("imgs/futurama-change-places.gif"))
    
    @commands.command()
    async def restore(self, context):
        """Restores nicknames manually"""
        guild = context.guild
        
        if str(context.message.author.id) in [config["gamemaster"][0]["ganj"]]:  # Checks if owner using command

            member_roles = [role for role in guild.roles if role.name == "Member"]

            perms = Permissions()  # Create a permissions object and remove the change nickname permission
            perms.update(change_nickname=True)

            for role in guild.roles:  # Go through every role in the server...
                if role == member_roles[0]:  # If we find the members role...
                    await role.edit(permissions=perms)  # Edit that role with removed permissions

                for member in guild.members:  # Go through every member in the guild...
                    if member_roles[0] in member.roles and member != guild.owner:  # If they have the "Members" role and aren't the owner...
                        await member.edit(nick=None)     # Make it so they have no nickname again!

            await context.send("```Restored members!```", delete_after=5)

        else:            
            await context.send("```You must not be a faggot to execute this command```", delete_after=5)


def setup(client):
    client.add_cog(ChangePlaces(client))