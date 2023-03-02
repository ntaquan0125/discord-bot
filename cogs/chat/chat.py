import time
import random
import requests

import openai
import discord

from discord.ext import commands

from utils import *


# Set up the OpenAI API client
openai.api_key = OPENAI_API_KEY


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model_engine = 'gpt-3.5-turbo'

    def get_response(self, prompt):
        completion = openai.ChatCompletion.create(
            model=self.model_engine,
            messages=[{"role": "user", "content": prompt}]
        )

        generated_text = completion['choices'][0]['message']['content'].strip('\n')
        return generated_text

    @commands.command()
    async def turbo(self, ctx, *, arg):
        generated_text = self.get_response(arg)
        await ctx.send(generated_text)


async def setup(bot):
    await bot.add_cog(Chat(bot))