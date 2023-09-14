import discord
from discord.ext.tasks import loop
from discord.ext.commands import Cog, Bot

import datetime

from utils import *
from typing import *

from database_bot_database import botDatabase

utc = datetime.timezone.utc

# set 8h30 time
time_birthday_check = datetime.time(hour=1, minute=30, tzinfo=utc)


class botTasks(Cog):
    def __init__(self, bot: Bot, database_handle: botDatabase):
        self.bot = bot
        self.database_handle = database_handle

        self.change_mode.start()
        self.birthday_check.start()

    async def send_birthday_messeage(self, name: str):
        pass

    @loop(hours=5.0)
    async def change_mode(self):
        staging = "your felling"
        await self.bot.change_presence(
            activity=discord.Game(staging), status=discord.Status.online
        )

    @change_mode.before_loop
    async def change_mode_before(self):
        await self.bot.wait_until_ready()

    @loop(time=time_birthday_check)
    async def birthday_check(self):
        today = datetime.date.today().strftime("%d/%m/%Y")
        search_topic = today[0:6] + "*"
        search_request = {"$regex": search_topic}
        search_result = await self.database_handle.find_with_filter(
            "birthday", search_request
        )

        if len(list(search_result.clone())) > 0:
            for cursor in search_result:
                await self.send_birthday_messeage(cursor["name"])
