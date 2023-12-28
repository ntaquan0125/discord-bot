from discord.ext import commands
from openai import OpenAI

from config import openai_api_key


class ChatGPTEngine:
    def __init__(self):
        # Set up the OpenAI API client
        self.client = OpenAI(api_key=openai_api_key)
        self.model_engine = 'gpt-3.5-turbo'

    def get_response(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model_engine,
            messages=[{"role": "user", "content": prompt}]
        )

        generated_text = completion['choices'][0]['message']['content'].strip('\n')
        return generated_text


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = ChatGPTEngine()

    @commands.command()
    async def chat(self, ctx, *, arg):
        generated_text = self.engine.get_response(arg)
        await ctx.send(generated_text)


async def setup(bot):
    await bot.add_cog(Chat(bot))
