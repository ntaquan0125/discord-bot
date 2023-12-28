import platform
import requests
import discord

from discord.ext import commands

from config import bot_version


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

        embed.add_field(name="**Bot Version:**", value=bot_version)
        embed.add_field(name="**Python Version:**", value=platform.python_version())
        embed.add_field(name="**Discord.Py Version**", value=discord.__version__)

        await ctx.channel.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        message = await ctx.send("Ping...")
        async with ctx.channel.typing():
            embed = discord.Embed(
                title="Pong!",
                description=f"Heartbeat: {round(self.bot.latency * 1000, 2)} ms",
                color=discord.Color.random(),
            )
            await message.edit(content="Done", embed=embed)

    @commands.command()
    async def sendNudes(self, ctx):
        try:
            response = requests.get("https://aws.random.cat/meow")
        except requests.exceptions.ConnectionError:
            return await ctx.send("Connection Error")
        data = response.json()
        embed = discord.Embed(title="Kitty Cat 🐈", colour=discord.Color.random())
        embed.set_image(url=data["file"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def poll(self, ctx, question, *options):
        if len(options) <= 1:
            await ctx.send('You need more than one option to create a poll!')
            return
        elif len(options) > 10:
            await ctx.send('You cannot create a poll with more than 10 options!')
            return

        reactions = ['1️⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        description = []
        for x, option in enumerate(options):
            description.append(f'{reactions[x]} {option}\n')
        embed = discord.Embed(
            title=question,
            description=''.join(description),
            colour=discord.Color.random()
        )
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text=f'Poll ID: {react_message.id}')
        await react_message.edit(embed=embed)
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(BotCommands(bot))
