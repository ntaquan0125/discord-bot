import asyncio
import json
import os
import sys
from pathlib import Path

import discord
from discord.ext.commands import Bot

from utils import *
from typing import *


parent_dir_path = str(Path(__file__).resolve().parents[1])
sys.path.append(parent_dir_path + "/src")
sys.path.append(parent_dir_path + "/src/modules/chat")
sys.path.append(parent_dir_path + "/src/modules/command")
sys.path.append(parent_dir_path + "/src/modules/event")
sys.path.append(parent_dir_path + "/src/modules/member")
sys.path.append(parent_dir_path + "/src/database")
sys.path.append(parent_dir_path + "/src/handler")

from member_management import botMemberManagement
from database_bot_database import botDatabase
from command import botCommands
from chat import botChatGPT

from handler_task_handler import botTasks
from handler_event_handler import botEvents

from utils import *

GUILD_ID = discord.Object(get_config_value("pif_guild_id"))


class botDiscord(Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all(),
        )

        self.database_handle = botDatabase(
            url=get_env_data("DATABASE_URL"),
            database_name=get_config_value("database_name"),
            collection_name=get_config_value("collection_name"),
        )

    async def setup_hook(self):
        print(f"{self.user} has connected to Discord!")

        await bot.add_cog(botCommands(bot=bot))
        await bot.add_cog(botChatGPT(bot=bot, api_key=get_env_data("OPENAI_API_KEY")))
        await bot.add_cog(
            botMemberManagement(bot=bot, database_handle=self.database_handle)
        )
        await bot.add_cog(botEvents(bot=bot))
        await bot.add_cog(botTasks(bot=bot, database_handle=self.database_handle))

        await bot.tree.sync()

    async def close(self) -> None:
        await super().close()


bot = botDiscord()
