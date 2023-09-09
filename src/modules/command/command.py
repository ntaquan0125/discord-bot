import platform
import requests
import random
import sys
from pathlib import Path

import discord

import aiohttp

from utils import *

from typing import *


parent_dir_path = str(Path(__file__).resolve().parents[0])
sys.path.append(parent_dir_path + "/src")

from client import client


class BotCommands:
    def __init__(self):
        pass

    async def info(self) -> discord.Embed:
        embed = discord.Embed(
            title="PIF Club's bot",
            description="Pay It Forward",
        )

        embed.add_field(name="**Bot Version:**", value=BOT_VERSION)
        embed.add_field(name="**Python Version:**", value=platform.python_version())
        embed.add_field(name="**Discord.Py Version**", value=discord.__version__)

        return embed

    async def random_cat(self) -> Union[discord.Embed, str]:
        try:
            main_url = "https://random.cat/view/" + str(random.randint(1, 1000))
            # response = requests.get(main_url)
            async with aiohttp.ClientSession() as session:
                async with session.get(main_url) as response:
                    if response.status == 200:
                        data = response.content._buffer[0].decode("utf-8")
                        img_url_start_loc = data.find("https://purr.objects")
                        for x in range(img_url_start_loc, len(data)):
                            if data[x] == '"':
                                img_url = data[img_url_start_loc:x]
                                break

                        embed = discord.Embed(
                            title="Kitty Cat 🐈", colour=discord.Color.random()
                        )
                        embed.set_image(url=img_url)

                        return embed

            return "Error fetching data"
        except Exception as e:
            print(e)
            return "Some thing error"

    async def ping(self) -> discord.Embed:
        embed = discord.Embed(
            title="Pong!",
            description=f"Heartbeat: {round(client.latency * 1000, 2)} ms",
            color=discord.Color.random(),
        )

        return embed


command = BotCommands()
