import asyncio
import discord
from discord.ext import commands
import json
import pytest
import os
import sys

from unittest import mock
import fatebot.main as main

# def test_client_start_async(monkeypatch):
#     monkeypatch.setattr(discord.Client, 'start', lambda x,y: print('MonkeyPatch'))    
#     bot = main.OracleBot()
#     bot.start(config["token"])
#     assert bot.is_ready() is False

# class MockOracleBot(MagickMock):
#     async def start(token):
#         conn = MagickMock()
#         f = asyncio.Future()
#         if token:
#             f.set_result(True)  
#         else:
#             f.set_result(False)

#         conn.start = MagicMock(return_value=f)

def test_main():
    fakeOracle = main.OracleBot()
    fakeOracle.start = mock.MagicMock(return_value=True)
    asyncio.run(main.main())
    fakeOracle.start.assert_called_once()
#    mock_start.assert_called_once()