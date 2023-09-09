import asyncio
import json
import os
import sys

from discord.ext import tasks
import discord

import openai
from openai.error import RateLimitError

from utils import *
from typing import *
from pathlib import Path

from client import client


class BotEvents:
    def __init__(self):
        pass

    @client.event
    async def on_member_join(member: discord.Member):
        await member.send(f"Hi {member.name}, welcome to {member.guild.name}!")

    @client.event
    async def on_member_remove(member: discord.Member):
        await member.send(f"Hi {member.name}, see ya :3 you have been kick!")

    @client.event
    async def on_member_ban(guild: discord.Guild, user: discord.Member):
        await user.send(
            f"Hi {user.name}, see ya :3 you have been ban from {guild.name}!"
        )

    @client.event
    async def on_member_unban(guild: discord.Guild, user: discord.Member):
        await user.send(
            f"Hi {user.name}, Your ban in {guild.name} have been revoke, you can join back!"
        )

    @client.event
    async def on_member_update(before: discord.Member, after: discord.Member):
        print("Some thing just happend")

    @client.event
    async def on_ready():
        client.ready = True
        print(f"Logged in as {client.user} (ID: {client.user.id})")
        print("------")
