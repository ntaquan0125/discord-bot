import asyncio
import json
import os
import sys

import discord

from discord import app_commands

from utils import *
from typing import *


class botClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)
        self.ready = False

    async def setup_hook(self):
        await self.tree.sync()


client = botClient()
