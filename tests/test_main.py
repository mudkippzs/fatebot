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


@pytest.fixture
def client():
    return OracleBot()


@mock.patch('main.OracleBot')
def test_main(mock_start):
    mock_start.start.return_value = True
    assert asyncio.run(main.main())
#    mock_start.assert_called_once()