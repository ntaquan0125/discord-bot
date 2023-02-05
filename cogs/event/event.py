import discord

from discord.ext import commands

from utils import *


class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to {GUILD}!'
        )
        

async def setup(bot):
    await bot.add_cog(BotEvents(bot))
