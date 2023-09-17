import discord
from discord.ext.tasks import loop
from discord.ext.commands import Cog, Bot

import datetime
import json
import random
import os

from utils import *
from typing import *

from database_bot_database import botDatabase

utc = datetime.timezone.utc

# set 8h30 time
time_birthday_check = datetime.time(
    hour=get_config_value("birthday_check_hour_utc"),
    minute=get_config_value("birthday_check_minute_utc"),
    tzinfo=utc,
)


class botTasks(Cog):
    def __init__(self, bot: Bot, database_handle: botDatabase):
        self.bot = bot
        self.database_handle = database_handle

        self.change_mode.start()

        if get_config_value("birdthday_check_enable") == "True":
            self.birthday_check.start()

    async def send_birthday_messeage(self, name: str):
        file_count = 0
        birthday_wishes_file_path = ""

        for path in os.scandir(BIRTHDAY_WISH_PATH):
            if os.path.isfile(path=path.path):
                file_count += 1

        if file_count == 1:
            birthday_wishes_file_path = BIRTHDAY_WISH_PATH + "1.txt"
        else:
            birthday_wishes_file_path = (
                BIRTHDAY_WISH_PATH + str(random.randint(1, file_count)) + ".txt"
            )

        with open(birthday_wishes_file_path) as birthday_wishes_file:
            birthday_wishes_file_contents = birthday_wishes_file.read()

        return birthday_wishes_file_contents.replace("<Name>", name)

    @loop(minutes=get_config_value("change_mode_time"))
    async def change_mode(self):
        with open(STATUS_FILE_PATH) as status_file:
            status_file_contents = json.loads(status_file.read())
        staging = status_file_contents["playing_status"][
            random.randint(0, len(list(status_file_contents["playing_status"])) - 1)
        ]
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
                birthday_wishes = await self.send_birthday_messeage(cursor["name"])
                user = await self.bot.fetch_user(cursor["discord_ID"])
                await user.send(birthday_wishes)

    @birthday_check.before_loop
    async def birthday_check_before(self):
        await self.bot.wait_until_ready()
