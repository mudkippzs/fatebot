"""
1. Make a Discord Task Dartboard that supports multiple channels.
2. Use a custom emoji react as a Dartboard trigger.
"""

import discord
from discord.ext import commands
import asyncio
import random
import re
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

from clogger import clogger

with open("config.json", "r") as f:
    config = json.load(f)


def load_json(file):
    with open(file, "r") as f:
        f = json.load(f)
    return f


def save_json(file, settings):
    with open(file, "w") as f:
        json.dump(settings, f)

    return


class MgDartboard(commands.Cog):

    """A starboard to upvote posts."""

    def __init__(self, bot):
        self.bot = bot
        self.settings_file = 'data/starboard/settings.json'
        self.settings = load_json(self.settings_file)

    @commands.group(pass_context=True, no_pm=True)
    async def dartboard(self, ctx):
        """Manage the starboard settings."""
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:

            if ctx.invoked_subcommand is None:
                await ctx.send(f"```No subcommand invoked: channel, emoji, threshold, toggle.```")

    @dartboard.command(name='channel', pass_context=True, no_pm=True)
    async def _channel(self, ctx, channel: discord.TextChannel):
        """Set the starboard channel."""
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:

            if not channel:
                await ctx.send('That channel does not exist.')
                return

            server = ctx.message.guild
            print(self.settings)
            self.settings[str(server.id)]["channel"] = channel.id
            save_json(self.settings_file, self.settings)
            await ctx.send('Dartboard channel set to {}.'.format(channel))

    @dartboard.command(name='emoji', pass_context=True, no_pm=True)
    async def _emoji(self, ctx, emoji: str):
        """Set the emoji for the starboard."""
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:

            if len(emoji) < 2:
                await ctx.send('That emoji is too small.')
                return

            server = ctx.message.guild
            self.settings[str(server.id)]['emoji'] = emoji
            save_json(self.settings_file, self.settings)
            await ctx.send('Dartboard emoji set to {}.'.format(emoji))

    @dartboard.command(name='limit', pass_context=True, no_pm=True)
    async def _limit(self, ctx, limit: int):
        """Set the minimum number of stars required to show up."""
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:

            server = ctx.message.guild
            self.settings[str(server.id)]['limit'] = limit
            save_json(self.settings_file, self.settings)
            await ctx.send('Dartboard limit set to {}.'.format(limit))

    @dartboard.command(name='age', pass_context=True, no_pm=True)
    async def _age(self, ctx, days: int):
        """Set the maximum age of a message valid for starring."""
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:

            server = ctx.message.guild
            self.settings[str(server.id)]['age'] = days
            save_json(self.settings_file, self.settings)
            await ctx.send('Maximum message age set to {}.'.format(days))

    @dartboard.command(name='toggle', pass_context=True, no_pm=True)
    async def _toggle(self, ctx):
        """Toggle the starboard on or off."""
        if str(ctx.message.author.id) in [config["gamemaster"][0]["ganj"]]:

            server = ctx.message.guild
            self.settings[str(server.id)]['toggle'] = not self.settings[str(
                server.id)]['toggle']
            save_json(self.settings_file, self.settings)
            if self.settings[str(server.id)]['toggle']:
                await ctx.send('Dartboard enabled.')
            else:
                await ctx.send('Dartboard disabled.')

    @commands.Cog.listener()
    async def on_ready(self):
        self.settings = load_json(self.settings_file)
        for server in self.bot.guilds:
            if str(server.id) not in self.settings.keys():
                self.settings[str(server.id)] = {
                    "channel": None,
                    "emoji": None,
                    "limit": None,
                    "age": None,
                    "toggle": None,
                }
        save_json(self.settings_file, self.settings)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        server = reaction.message.guild
        if reaction.message.channel.id == 938444879682478121:
            message = reaction.message
            if str(server.id) not in self.settings.keys():
                return

            if self.settings[str(server.id)]['toggle'] is False:
                return

            if user == message.author:
                return

            if str(reaction.emoji) != self.settings[str(server.id)]['emoji']:
                return

            channel = message.channel

            stars = reaction.count  # The bot's reaction shouldn't count
            if stars < self.settings[str(server.id)]['limit']:
                return

            if message.channel == self.get_starboard(server):
                return

            dartboard_channel = self.get_starboard(server)
            embed = discord.Embed(
                title=f"{message.author.display_name} in {message.channel.name}")
            embed.add_field(name="Original Post",
                            value=f"```{message.clean_content}```")
            embed.set_thumbnail(url=message.author.avatar_url)
            attachment_list = [{"filename": a.filename, "contenttype": a.content_type,
                                "filesize": a.size, "url": a.url} for a in message.attachments]
            for attachment in attachment_list:
                for key, ele in enumerate(attachment):
                    embed.add_field(name=f"{key}", value=f"```{ele[key]}```")

            await dartboard_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        server = reaction.message.guild
        message = reaction.message
        if reaction.message.channel.id == 938444879682478121:
            if server.id not in self.settings:
                return
            if self.settings[str(server.id)]['toggle'] is False:
                return
            if user == message.author:
                return
            if reaction.emoji != self.settings[str(server.id)]['emoji']:
                return

            channel = message.channel

            stars = reaction.count - 1  # The bot's reaction shouldn't count
            if stars < self.settings[str(server.id)]['limit']:
                return

            if message.channel == self.get_starboard(server):
                return

    def get_starboard(self, server):
        dartboard_channel = self.settings[str(server.id)]['channel']
        return server.get_channel(dartboard_channel)


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def check_folders():
    if not os.path.exists('data/starboard'):
        print('Creating data/starboard folder...')
        os.makedirs('data/starboard')


def check_files():
    f = 'data/starboard/settings.json'
    if not is_json(f):
        print('Creating default settings.json...')
        save_json(f, {})


def setup(bot):
    bot.add_cog(MgDartboard(bot))
