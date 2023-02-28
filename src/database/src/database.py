import discord
from discord.ext import commands
from discord import app_commands

MY_GUILD = discord.Object(id=766586939498823690)

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="cat>", intents=intents)
