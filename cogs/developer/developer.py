import discord

from discord.ext import commands

from utils import *


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load')
    @commands.is_owner()
    async def load_extension(self, ctx, extension_name: str):
        extension_name = extension_name.lower()
        try:
            cogs_dir = 'cogs'
            await self.bot.load_extension(cogs_dir + '.' + extension_name + '.' + extension_name)
            await ctx.send(f'Extension `{extension_name}` loaded!')
        except commands.ExtensionError:
            await ctx.send(f'Failed to load extension `{extension_name}`.')

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload_extension(self, ctx, extension_name: str):
        extension_name = extension_name.lower()
        if extension_name == 'developer':
            await ctx.send(f"You can't unload `{extension_name}`!")
        try:
            cogs_dir = 'cogs'
            await self.bot.unload_extension(cogs_dir + '.' + extension_name + '.' + extension_name)
            await ctx.send(f'Extension `{extension_name}` unloaded!')
        except commands.ExtensionError:
            await ctx.send(f'Failed to unload extension `{extension_name}`.')

    @commands.command(name='reload')
    @commands.is_owner()
    async def reload_extension(self, ctx, extension_name: str):
        extension_name = extension_name.lower()
        if extension_name == 'developer':
            await ctx.send(f"You can't reload `{extension_name}`!")
        try:
            cogs_dir = 'cogs'
            await self.bot.unload_extension(cogs_dir + '.' + extension_name + '.' + extension_name)
            await self.bot.load_extension(cogs_dir + '.' + extension_name + '.' + extension_name)
            await ctx.send(f'Extension `{extension_name}` reloaded!')
        except commands.ExtensionError:
            await ctx.send(f'Failed to reload extension `{extension_name}`.')


async def setup(bot):
    await bot.add_cog(Developer(bot))