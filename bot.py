import asyncio
import json
import logging
import logging.handlers
import os
import sys

import discord

from discord.ext import commands

from utils import *


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='cat>', intents=intents)

# Redirect error to stderr
logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)


@bot.event
async def setup_hook():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if not bot.is_ready:
        return

    # Do not process commands in a listener, only in the event
    await bot.process_commands(message)


async def main():
    cogs_dir = 'cogs'
    for extension in [dirs for dirs in os.listdir(cogs_dir) if os.path.isdir(os.path.join(cogs_dir, dirs))]:
        try:
            await bot.load_extension(cogs_dir + '.' + extension + '.' + extension)
        except commands.ExtensionError as e:
            print(f'Failed to load extension {extension}.')
            print(e)
    await bot.start(TOKEN)


asyncio.run(main())