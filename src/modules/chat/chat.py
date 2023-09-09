import asyncio
import json
import os
import sys

import discord
import openai
from openai.error import RateLimitError

from utils import *
from typing import *
from pathlib import Path

parent_dir_path = str(Path(__file__).resolve().parents[1])
sys.path.append(parent_dir_path + "/src")

from client import client


# Set up the OpenAI API client
openai.api_key = "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"


class ChatGPT:
    def __init__(self):
        self.model_engine = "gpt-3.5-turbo"

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


chat = ChatGPT()
