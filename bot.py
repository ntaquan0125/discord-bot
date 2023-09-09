import asyncio
import json
import os
import sys

import discord

from utils import *
from typing import *
from pathlib import Path

parent_dir_path = str(Path(__file__).resolve().parents[0])
sys.path.append(parent_dir_path + "/src")
sys.path.append(parent_dir_path + "/src/modules/chat")
sys.path.append(parent_dir_path + "/src/modules/command")
sys.path.append(parent_dir_path + "/src/modules/event")
sys.path.append(parent_dir_path + "/src/database/src")
sys.path.append(parent_dir_path + "/src/handler")

from client import client
from chat import chat
from command import command
from event_handler import BotEvents
from task_handler import TaskEvents
from database import BotDatabase

EventHandle = BotEvents()
TaskHandle = TaskEvents(client=client)
DatabaseHandle = BotDatabase(
    "mongodb://root:password@mongo:27017/?authSource=admin",
    "member_PIF",
    "discord_database",
)


@client.tree.command(
    name="test",
    description="test",
)
async def test(interaction: discord.Interaction):
    print(interaction.user.name)
    await interaction.user.send("asd")


@client.tree.command(
    name="gpt",
    description="Not real GPT",
)
async def gpt(interaction: discord.Interaction, gpt_question: str):
    generated_text = chat.get_response(gpt_question)
    await interaction.response.send_message(generated_text)


@client.tree.command(
    name="cat",
    description="Just cat",
)
async def cat(interaction: discord.Interaction):
    return_data = await command.random_cat()
    if type(return_data) == str:
        await interaction.response.send_message(return_data, ephemeral=True)
    else:
        await interaction.response.send_message("", embed=return_data, ephemeral=False)


@client.tree.command(
    name="info",
    description="Just info",
)
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "", embed=await command.info(), ephemeral=True
    )


@client.tree.command(
    name="ping",
    description="Just ping",
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        "", embed=await command.ping(), ephemeral=True
    )


async def main():
    await asyncio.gather(
        client.start(
            "ODIwMTg5NzA3ODY2MjEwMzE0.GJ0KL8.XasZ32SnzVni1KRPcxh69a-mvcv_qkjoNeNFT8"
        ),
        TaskHandle.change_mode(),
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
