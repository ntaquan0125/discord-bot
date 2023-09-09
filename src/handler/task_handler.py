import asyncio
import json
import os
import sys

from discord.ext import tasks
import discord

import openai
from openai.error import RateLimitError

from utils import *
from typing import *
from pathlib import Path


class TaskEvents:
    def __init__(self, client: discord.Client):
        self.client = client

    # @tasks.loop(seconds=5)
    async def change_mode(self):
        while 1:
            print("Loop")
            await asyncio.sleep(10)
            if self.client.ready == True:
                await self.client.change_presence(
                    activity=discord.Game("your felling"), status=discord.Status.online
                )
