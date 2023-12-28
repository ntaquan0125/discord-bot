import discord
import psutil

from discord.ext import commands

from config import *


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, name='load')
    @commands.is_owner()
    async def load_extension(self, ctx, extension_name):
        extension_name = extension_name.lower()
        try:
            cogs_dir = self.bot.cogs_dir
            await self.bot.load_extension(cogs_dir + ('.' + extension_name) * 2)
            await ctx.send(f'Extension `{extension_name}` loaded!')
        except commands.ExtensionError:
            await ctx.send(f'Failed to load extension `{extension_name}`.')

    @commands.command(hidden=True, name='unload')
    @commands.is_owner()
    async def unload_extension(self, ctx, extension_name):
        extension_name = extension_name.lower()
        if extension_name == 'admin':
            await ctx.send(f"You can't unload `{extension_name}`!")
        try:
            cogs_dir = self.bot.cogs_dir
            await self.bot.unload_extension(cogs_dir + ('.' + extension_name) * 2)
            await ctx.send(f'Extension `{extension_name}` unloaded!')
        except commands.ExtensionError:
            await ctx.send(f'Failed to unload extension `{extension_name}`.')

    @commands.command(hidden=True, name='reload')
    @commands.is_owner()
    async def reload_extension(self, ctx, extension_name):
        extension_name = extension_name.lower()
        if extension_name == 'admin':
            await ctx.send(f"You can't reload `{extension_name}`!")
        try:
            cogs_dir = self.bot.cogs_dir
            await self.bot.unload_extension(cogs_dir + ('.' + extension_name) * 2)
            await self.bot.load_extension(cogs_dir + ('.' + extension_name) * 2)
            await ctx.send(f'Extension `{extension_name}` reloaded!')
        except commands.ExtensionError:
            await ctx.send(f'Failed to reload extension `{extension_name}`.')

    @commands.command(hidden=True)
    async def debug(self, ctx):
        embed = discord.Embed(
            title='Debug info',
            colour=discord.Color.random()
        )

        current_extensions = [cog.lower() for cog in self.bot.cogs]
        embed.add_field(name='Loaded extensions', value=', '.join(current_extensions), inline=False)

        current_memory = psutil.virtual_memory()[1] / 1024**3
        total_memory = psutil.virtual_memory()[0] / 1024**3
        embed.add_field(name="Server memory", value=str(round(current_memory)) + "GB / "
            + str(round(total_memory)) + "GB", inline=True)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))