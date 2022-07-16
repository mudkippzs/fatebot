import glob
import sys
sys.path += ['/home/dev/Code/']

import pytest
import discord.ext.test as dpytest

import fatebot.main as main

@pytest.fixture
def bot(event_loop):
    bot = main.OracleBot() # However you create your bot, make sure to use loop=event_loop
    dpytest.configure(bot)
    return bot


def pytest_sessionfinish():
    # Clean up attachment files
    files = glob.glob('./dpytest_*.dat')
    for path in files:
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error while deleting file {path}: {e}")