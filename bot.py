import asyncio
import json
import os
import sys

import discord

from discord.ext import commands
from discord import app_commands

from utils import *
from typing import *
from pathlib import Path

parent_dir_path = str(Path(__file__).resolve().parents[0])
sys.path.append(parent_dir_path + "/src/database/src")

from database import *


@bot.event
async def setup_hook():
    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if not bot.is_ready:
        return

    # Do not process commands in a listener, only in the event
    await bot.process_commands(message)


async def main():
    cogs_dir = "cogs"
    except_list = ["__pycache__", "lib"]
    for extension in [
        dirs
        for dirs in os.listdir(cogs_dir)
        if os.path.isdir(os.path.join(cogs_dir, dirs))
    ]:
        if extension in except_list:
            continue
        try:
            await bot.load_extension(cogs_dir + "." + extension + "." + extension)
        except Exception as e:
            print(e)
            print(f"Failed to load extension {extension}.")

    print(bot.tree.get_commands())
    print(bot.tree.context_menu())
    await bot.start(TOKEN)


asyncio.run(main())
