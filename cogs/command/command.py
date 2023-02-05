import platform
import requests

import discord

from discord.ext import commands

from utils import *

from .modules.database import botDatabase


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title="PIF Club's bot",
            description="Pay It Forward",
            color=ctx.author.colour,
        )

        embed.add_field(name="**Bot Version:**", value=BOT_VERSION)
        embed.add_field(name="**Python Version:**", value=platform.python_version())
        embed.add_field(name="**Discord.Py Version**", value=discord.__version__)

        await ctx.channel.send(embed=embed)

    @commands.command()
    async def sendNudes(self, ctx):
        response = requests.get("https://aws.random.cat/meow")
        data = response.json()
        embed = discord.Embed(title="Kitty Cat 🐈", colour=discord.Color.random())
        embed.set_image(url=data["file"])
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        msg = await ctx.send("Ping...")
        async with ctx.channel.typing():
            embed = discord.Embed(
                title="Pong!",
                description=f"Heartbeat: {round(self.bot.latency * 1000, 2)} ms",
                color=discord.Color.random(),
            )
            await msg.edit(content="Done", embed=embed)

    @commands.command()
    async def filters(ctx):
        pass

    @commands.command()
    async def help(ctx):
        pass


async def setup(bot):
    await bot.add_cog(BotCommands(bot))
