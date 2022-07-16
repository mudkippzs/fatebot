"""Discord Bot: Fatebot
Author: Ganjdalf
"""
import asyncio
from pathlib import Path
import json
import os
import sys


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '.')))

from clogger import clogger
import discord
from cogwatch import watch
from discord.ext import commands
from discord_components import ComponentsBot

with open("config.json", "r") as f:
    config = json.load(f)

with open("strings.json", "r") as f:
    strings = json.load(f)

# Declare Bots required perms via Intents().
INTENTS = discord.Intents.all()

class OracleBot(ComponentsBot):
    """A bot for managing a discord server that extends discord.py Bot class."""

    def __init__(self):
        """Kick off instance of Fatebot."""
        super().__init__(
            command_prefix=config["prefix"],
            description=strings["strings"]["welcome_message"],
            intents=INTENTS)
        self.load_extensions()

    def load_extensions(self):
        """Load extensions on start of the bot."""
        for ext in Path("cogs").glob("./*.py"):
            dot_path = str(ext).replace(os.sep, ".")[:-3]
            self.load_extension(dot_path)
            clogger(f"Cog loaded: {dot_path}")

    @watch(path='cogs', debug=False)
    async def on_ready(self):
        """Client Even - on_ready: triggers when Client is logged in and listening for events."""
        clogger(f"{self.user} is online!")


async def main():
    """Create the bot and start it."""
    client = OracleBot()
    await client.start(config["token"])

if __name__ == '__main__':
    asyncio.run(main())
