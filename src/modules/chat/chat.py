import asyncio
import json
import os
import sys

import discord
from discord.ext.commands import Cog
from discord import app_commands

import openai
from openai.error import RateLimitError

from utils import *
from typing import *
from pathlib import Path

parent_dir_path = str(Path(__file__).resolve().parents[1])
sys.path.append(parent_dir_path + "/src")


class botChatGPT(Cog):
    def __init__(self, bot, api_key):
        super().__init__()

        self.bot = bot

        self.model_engine = "gpt-3.5-turbo"
        openai.api_key = api_key

    def get_response(self, prompt):
        try:
            completion = openai.Completion.create(
                engine=self.model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            generated_text = completion.choices[0].text.strip("\n")
        except RateLimitError:
            return "Rate Limit Error"
        except Exception as e:
            return e

        return generated_text

    @app_commands.command(
        name="gpt",
        description="Use GPT chat, it doesn't work right now",
    )
    @app_commands.describe(gpt_question="Question for GPT")
    async def gpt(self, interaction: discord.Interaction, gpt_question: str):
        generated_text = self.get_response(gpt_question)
        await interaction.response.send_message(generated_text)
