import discord
from discord.ext import commands
import json
import os
import random
import re
import sys

from typing import List, Dict, Union, Optional

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger
from split_text import split_text

with open("config.json", "r") as f:
    config = json.load(f)


def convert_perms(perms):
    """
    Convert a list of Discord perms to a Discord permissions 53-bit integer value.
    """
    # Create a list of all the permissions that are true.
    true_perms = []
    for perm in perms:
        if perm[1] == True:
            true_perms.append(perm[0])

    # Convert the list of permissions to a bitmask.
    bitmask = 0b0
    for perm in true_perms:
        if perm == "create_instant_invite":
            bitmask = bitmask | 0b00000001
        elif perm == "kick_members":
            bitmask = bitmask | 0b00000010
        elif perm == "ban_members":
            bitmask = bitmask | 0b00000100
        elif perm == "administrator":
            bitmask = bitmask | 0b00001000
        elif perm == "manage_channels":
            bitmask = bitmask | 0b00010000
        elif perm == "manage_guild":
            bitmask = bitmask | 0b00100000
        elif perm == "add_reactions":
            bitmask = bitmask | 0b01000000
        elif perm == "view_audit_log":
            bitmask = bitmask | 0b10000000
        elif perm == "priority_speaker":
            bitmask = bitmask | 0b100000000
        elif perm == "stream":
            bitmask = bitmask | 0b1000000000
        elif perm == "read_messages":
            bitmask = bitmask | 0b10000000000
        elif perm == "send_messages":
            bitmask = bitmask | 0b100000000000
        elif perm == "send_tts_messages":
            bitmask = bitmask | 0b1000000000000
        elif perm == "manage_messages":
            bitmask = bitmask | 0b10000000000000
        elif perm == "embed_links":
            bitmask = bitmask | 0b100000000000000
        elif perm == "attach_files":
            bitmask = bitmask | 0b1000000000000000
        elif perm == "read_message_history":
            bitmask = bitmask | 0b10000000000000000
        elif perm == "mention_everyone":
            bitmask = bitmask | 0b100000000000000000
        elif perm == "external_emojis":
            bitmask = bitmask | 0b1000000000000000000
        elif perm == "view_guild_insights":
            bitmask = bitmask | 0b10000000000000000000
        elif perm == "connect":
            bitmask = bitmask | 0b100000000000000000000
        elif perm == "speak":
            bitmask = bitmask | 0b1000000000000000000000
        elif perm == "mute_members":
            bitmask = bitmask | 0b10000000000000000000000
        elif perm == "deafen_members":
            bitmask = bitmask | 0b100000000000000000000000
        elif perm == "move_members":
            bitmask = bitmask | 0b1000000000000000000000000
        elif perm == "use_voice_activation":
            bitmask = bitmask | 0b10000000000000000000000000
        elif perm == "change_nickname":
            bitmask = bitmask | 0b100000000000000000000000000
        elif perm == "manage_nicknames":
            bitmask = bitmask | 0b1000000000000000000000000000
        elif perm == "manage_roles":
            bitmask = bitmask | 0b10000000000000000000000000000
        elif perm == "manage_webhooks":
            bitmask = bitmask | 0b100000000000000000000000000000
        elif perm == "manage_emojis":
            bitmask = bitmask | 0b1000000000000000000000000000000
        elif perm == "use_slash_commands":
            bitmask = bitmask | 0b10000000000000000000000000000000
        elif perm == "request_to_speak":
            bitmask = bitmask | 0b100000000000000000000000000000000
    return bitmask


def strip_tags(string):
    """
    This function will strip all html tags from string returning the inner html text using regex only.
    """
    return re.sub('<.*?>', '', string)

def check_db_exists(guild_id):
    filename = f"./dbs/roles_{guild_id}.json"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            clogger(exc)
            raise exc

def open_json(guild_id):
    check_db_exists(guild_id)
    filename = f"./dbs/roles_{guild_id}.json"
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("{\"roles\":[]}")
    with open(filename) as f:
        return json.load(f)


class Moderation(commands.Cog):
    """Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purgemessages"])
    async def purge(self, ctx, limit: int, member: discord.Member = None):
        """Owner only - Delete messages from a channel."""
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:
            if member is None:
                await ctx.channel.purge(limit=limit)
            else:
                await ctx.channel.purge(limit=limit, check=lambda m: m.author == member)
        else:
            await ctx.send("```Sorry, only the owner can purge messages.```", delete_after=5.0)

    # Export the Roles

    @commands.command(aliases=["exportroles", "exprol"])
    async def export_roles(self, ctx):
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:
            guild = ctx.guild
            guild_whitelist = [832999632028041226]
            if guild.id in guild_whitelist:
                check_db_exists(guild.id)
                roles = {"roles": []}
                for guild_role in guild.roles:
                    clogger(guild_role)
                    roles["roles"].append(
                        [guild_role.name,
                         guild_role.id,
                         [p for p in guild_role.permissions],
                         guild_role.guild.id,
                         guild_role.position])

                with open(f"./dbs/roles_{guild.id}.json", "w") as roles_file:
                    json.dump(roles, roles_file, indent=4)

                await ctx.send('Roles exported to roles.json')
            else:
                await ctx.send("This command is not available for this server.")
        else:
            await ctx.send("You do not have permission to use this command.")

    @commands.command(aliases=["importroles", "improl"])
    async def import_roles(self, ctx):
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:
            guild = ctx.guild
            guild_whitelist = [832999632028041226]
            if guild.id in guild_whitelist:
                roles = open_json(guild.id)

                for guild_role in guild.roles:
                    for role in roles["roles"]:
                        if role[1] == guild_role.id:
                            try:
                                await guild_role.edit(name=role[0], position=role[4], permissions=discord.Permissions(convert_perms(role[2])))
                            except Exception as e:
                                pass
                            break
                await ctx.send('Roles imported from roles.json')
            else:
                await ctx.send('This command is not available for this server.')
        else:
            await ctx.send('You do not have permission to use this command.')


def setup(client):
    client.add_cog(Moderation(client))
