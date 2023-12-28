import os
import discord

from discord.ext import commands

from config import debug


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='cat>', intents=intents)
        self.cogs_dir = 'cogs'

    async def setup_hook(self):
        print(f'{self.user.name} has connected to Discord!')

        available_extensions = [dirs for dirs in os.listdir(self.cogs_dir) 
                                if os.path.isdir(os.path.join(self.cogs_dir, dirs))]
        for extension in available_extensions:
            try:
                await self.load_extension(self.cogs_dir + ('.' + extension) * 2)
                print(f'Loaded extension {extension}.')
            except commands.ExtensionError as e:
                print(f'Failed to load extension {extension}.')

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        if not self.is_ready:
            return

        # Do not process commands in a listener, only in the event
        await self.process_commands(message)
    
    async def on_command_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the necessary permissions to use this command.')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        
        if debug:
            print(str(error))