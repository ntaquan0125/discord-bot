import discord
import sys

from discord.ext import commands
from discord import app_commands

from utils import *

from typing import *
from pathlib import Path

parent_dir_path = str(Path(__file__).resolve().parents[4])
sys.path.append(parent_dir_path + "/cogs/lib/database/src")

from mysql import *
from database import *


class BotFilters(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @bot.tree.command(name="filters", description="testing", guild=MY_GUILD)
    async def add_filters(self, interaction: discord.Interaction, name: str, data: str):
        await interaction.response.send_message("Add" + data)

    @bot.tree.command(name="remove", description="testing", guild=MY_GUILD)
    async def remove_filters(self, interaction: discord.Interaction, name: str):
        await interaction.response.send_message("Remove" + name)


async def setup(bot):
    await bot.add_cog(BotFilters(bot))
