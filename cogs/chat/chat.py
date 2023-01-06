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
        self.model_engine = 'text-davinci-003'

    def get_response(self, prompt):
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        generated_text = completion.choices[0].text.strip('\n')
        return generated_text

    @commands.command()
    async def chat(self, ctx, *, arg):
        try:
            generated_text = self.get_response(arg)
            await ctx.send(generated_text)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Chat(bot))
