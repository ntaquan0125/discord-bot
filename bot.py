# bot.py
import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response_list = [
        'thế kỷ 21 rồi ai cũng làm wjbu',
        'chạn vương muôn năm',
        'làm gì thì làm đừng làm thinh là được',
        'tao sắp ra trường rồi',
        'bug vler'
    ]

    if message.content == 'cat':
        response = random.choice(message_list)
        await message.channel.send(response)

client.run(TOKEN)