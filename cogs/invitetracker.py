import discord
from discord.ext import commands
import json
import logging
import os
import random
import re
import sys

import asyncio
import time

from datetime import datetime, timedelta
from collections import Counter
from itertools import islice
from typing import List, Dict, Union, Optional

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger


class InviteLog(commands.Cog):

    settings = None

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("inviteloglog")
        self.invite_file = "data/invitelog/settings.json"

    @commands.Cog.listener()
    async def on_ready(self):
        self.load()  # load invite management db.
        for guild in self.bot.guilds:
            if str(guild.id) not in self.settings.keys():
                self.settings[str(guild.id)] = {"invite_log_channel": None}
        self.save()

    def load(self):
        """Load the timezone data from the json file."""
        if os.path.isfile(self.invite_file):
            with open(self.invite_file, "r") as f:
                self.settings = json.load(f)
            clogger("Invitelog DB loaded.")
            # clogger(self.tz_data)
        else:
            clogger("Couldn't load Invitelog DB.")

    def save(self):
        """Save the timezone data to the json file."""
        with open(self.invite_file, "w") as f:
            json.dump(self.settings, f)

    @commands.command(pass_context=True)
    async def setinvitelogchannel(self, ctx, channel: discord.TextChannel):
        """Set the invite log channel."""

        clogger(self.settings)

        # Check if the channel is a text channel.
        if channel.type != discord.ChannelType.text:
            await ctx.send("That's not a text channel.")

        # Check if the channel is in the same server as the command was used in.
        if ctx.message.guild.id != channel.guild.id:
            await ctx.send("That's not a channel in this server.")

        # Check if the channel is already set as the invite log channel.
        if channel.id == self.settings[str(ctx.message.guild.id)]["invite_log_channel"]:
            await ctx.send("That channel is already set as the invite log channel.")

        # Set the invite log channel.
        self.settings[str(ctx.guild.id)]["invite_log_channel"] = channel.id

        self.save()

        await ctx.send(f"The invite log channel has been set to {self.settings[str(ctx.guild.id)]['invite_log_channel']}.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Log when a member joins the server."""

        # Get the server object for the server the member joined.
        server = member.guild

        # Get the invite log channel object for the server the member joined.
        invite_log_channel = discord.utils.get(
            server.channels, id=self.settings[str(server.id)]["invite_log_channel"])

        # Check if the invite log channel is set for the server the member joined.
        if not invite_log_channel:
            return

        # Get all invites for the server the member joined and sort them by uses.
        invites = await server.invites()
        invites = sorted(invites, key=lambda x: x.uses, reverse=True)

        # Get the invite object for the invite the member used to join the server.
        invite = discord.utils.find(lambda x: x.id == member.id, invites)

        # Get the inviter object for the invite the member used to join the server.
        inviter = discord.utils.find(
            lambda x: x.id == invite.inviter.id, server.members)

        # Get the server member count for the server the member joined.
        server_member_count = len(server.members)

        # Create a list of fields for the embed message.
        fields = [
            ("Inviter", inviter, True),
            ("Channel", invite.channel.mention, True),
            ("Invite Rank", invite.channel.mention, True),
            ("Invite Uses", invite.uses, True),
            ("Account Created", member.created_at, True),
            ("Member Count", server_member_count, True),
        ]

        # Create the embed message.
        embed = discord.Embed(title="Member Joined", description="{} joined the server.".format(
            member.mention), color=0x00FF00)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="User ID: " + member.id)

        # Send the embed message to the invite log channel.
        await self.bot.send_message(invite_log_channel, embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Log when a member leaves the server."""

        # Get the server object for the server the member left.
        server = member.guild

        # Get the invite log channel object for the server the member left.
        invite_log_channel = discord.utils.get(
            server.channels, id=self.settings[str(server.id)]["invite_log_channel"])

        # Check if the invite log channel is set for the server the member left.
        if not invite_log_channel:
            return

        # Get all invites for the server the member left and sort them by uses.
        invites = await server.invites()
        invites = sorted(invites, key=lambda x: x.uses, reverse=True)

        # Get the invite object for the invite the member used to join the server.
        invite = discord.utils.find(lambda x: x.id == member.id, invites)

        # Get the inviter object for the invite the member used to join the server.
        inviter = discord.utils.find(
            lambda x: x.id == invite.inviter.id, server.members)

        # Get the real invite count for the invite the member used to join the server.
        real_invite_count = invite.uses - 1

        # Get the invite rank for the invite the member used to join the server.
        invite_rank = invites.index(invite) + 1

        # Get the account age for the member who joined the server.
        account_age = (datetime.utcnow() - member.created_at).days

        # Get the server member count for the server the member joined.
        server_member_count = len(server.members)

        # Create a list of fields for the embed message.
        fields = [
            ("Inviter", inviter, True),
            ("Channel", invite.channel.mention, True),
            ("Invite Rank", invite.channel.mention, True),
            ("Invite Uses", invite.uses, True),
            ("Account Created", member.created_at, True),
            ("Member Count", server_member_count, True),
        ]

        # Create the embed message.
        embed = discord.Embed(title="Member Left", description="{} left the server.".format(
            member.mention), color=0xFF0000, timestamp=invite.created_at)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="User ID: " + member.id)

        # Send the embed message to the invite log channel.
        await invite_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        """Log when an invite is created."""
        self.load()

        # Get the server object for the server the invite was created in.
        server = invite.guild

        # Get the invite log channel object for the server the invite was created in.
        invite_log_channel = discord.utils.get(
            server.channels, id=self.settings[str(server.id)]["invite_log_channel"])

        # Check if the invite log channel is set for the server the invite was created in.
        if not invite_log_channel:
            return

        # Get all invites for the server the invite was created in and sort them by uses.
        invites = await server.invites()
        invites = sorted(invites, key=lambda x: x.uses, reverse=True)

        # Get the inviter object for the invite that was created.
        inviter = discord.utils.find(
            lambda x: x.id == invite.inviter.id, server.members)

        # Get the real invite count for the invite that was created.
        real_invite_count = invite.uses

        # Get the invite rank for the invite that was created.
        invite_rank = invites.index(invite) + 1

        # Create a list of fields for the embed message.
        fields = [
            ("Inviter", inviter, True),
            ("Channel", invite.channel.mention, True),
            ("Member Count", server_member_count, True),
        ]

        # Create the embed message.
        embed = discord.Embed(
            title="Invite Created", description="An invite was created.", color=0x0000FF, timestamp=invite.created_at)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Invite Code: " + invite.code)

        # Send the embed message to the invite log channel.
        await invite_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        """Log when an invite is deleted."""
        self.load()

        # Get the server object for the server the invite was deleted in.
        server = invite.guild

        # Get the invite log channel object for the server the invite was deleted in.
        invite_log_channel = discord.utils.get(
            server.channels, id=self.settings[str(server.id)]["invite_log_channel"])

        # Check if the invite log channel is set for the server the invite was deleted in.
        if not invite_log_channel:
            return

        # Get all invites for the server the invite was deleted in and sort them by uses.
        invites = await server.invites()
        invites = sorted(invites, key=lambda x: x.uses, reverse=True)

        # Get the inviter object for the invite that was deleted.
        clogger(invite.inviter)
        clogger(invite.code)
        clogger(invite.guild)
        clogger(invite.channel)
        clogger(invite.created_at)
        clogger(invite.url)
        inviter = discord.utils.find(
            lambda x: x.id == invite.inviter.id, server.members)

        # Get the real invite count for the invite that was deleted.
        real_invite_count = invite.uses

        # Get the invite rank for the invite that was deleted.
        invite_rank = invites.index(invite) + 1

        # Create a list of fields for the embed message.
        fields = [
            ("Inviter", inviter, True),
            ("Channel", invite.channel.mention, True),
            ("Invite Rank", invite.channel.mention, True),
            ("Invite Uses", invite.uses, True),
            ("Member Count", server_member_count, True),
        ]
        # Create the embed message.
        embed = discord.Embed(
            title="Invite Deleted", description="An invite was deleted.", color=0xFF0000, timestamp=invite.created_at)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Invite Code: " + invite.code)

        # Send the embed message to the invite log channel.
        await invite_log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(InviteLog(bot))
