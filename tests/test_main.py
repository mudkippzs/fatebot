import sys
sys.path += ['/home/dev/Code/']

import asyncio
import pytest
import discord.ext.test as dpytest


import fatebot.main as main

@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("?boons")
    assert dpytest.verify().message().contains().content("Searching for a boon containg the term")