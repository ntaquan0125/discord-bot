from discord.ext import commands

from utils import *


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Developer(bot))
