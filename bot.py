import asyncio
import json
import os
import sys

import discord

from typing import *
from pathlib import Path

parent_dir_path = str(Path(__file__).resolve().parents[0])
sys.path.append(parent_dir_path + "/src")
sys.path.append(parent_dir_path + "/src/modules/chat")
sys.path.append(parent_dir_path + "/src/modules/command")
sys.path.append(parent_dir_path + "/src/modules/event")
sys.path.append(parent_dir_path + "/src/modules/member")
sys.path.append(parent_dir_path + "/src/database")
sys.path.append(parent_dir_path + "/src/handler")

from client import bot
from utils import *

bot.run(token=get_env_data("DISCORD_TOKEN"))
