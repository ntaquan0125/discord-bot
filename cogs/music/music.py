import asyncio
import random

import discord
import yt_dlp as youtube_dl

from typing import Union
from discord.ext import commands

from utils import *


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',    # Bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # Take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    @commands.command(brief='Join a voice chat')
    async def join(self, ctx, *, channel: Union[discord.VoiceChannel, None]):
        if channel is None and ctx.author.voice:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(brief='Play music from a given URL')
    async def play(self, ctx, *, url):
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=False)

        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = [player]
        else:
            self.queues[ctx.guild.id].append(player)
            await ctx.send(f'{player.title} has been sent to queue.')
        self.play_from_queue(ctx)

    def play_from_queue(self, ctx):
        if not ctx.voice_client.is_playing():
            if len(self.queues[ctx.guild.id]) > 0:
                player = self.queues[ctx.guild.id].pop(0)
                ctx.voice_client.play(player, after=lambda e: print(e) if e else self.play_from_queue(ctx))

    @commands.command(brief='Pause the audio playing')
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Audio is paused.")
        else:
            await ctx.send("Currently no audio is playing.")

    @commands.command(brief='Resume the audio playing')
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed audio.")
        else:
            await ctx.send("The audio is not paused.")

    @commands.command(brief='Changes volume')
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(brief='Stop playing audio')
    async def stop(self, ctx):
        await ctx.voice_client.stop()

    @commands.command(brief='Leave the current voice channel')
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(brief='Display the current song queue')
    async def queue(self, ctx):
        description = []
        for i, song in enumerate(self.queues[ctx.guild.id]):
            description += f'\n{i}) {song.title}'
        embed = discord.Embed(
            title='Song queue',
            description=''.join(description),
            colour=discord.Color.random()
        )
        await ctx.send(embed=embed)

    @commands.command(brief='Shuffle the queue')
    async def shuffle(self, ctx):
        random.shuffle(self.queues[ctx.guild.id])
        description = []
        for i, song in enumerate(self.queues[ctx.guild.id]):
            description += f'\n{i}) {song.title}'
        embed = discord.Embed(
            title='Song queue',
            description=''.join(description),
            colour=discord.Color.random()
        )
        await ctx.send(embed=embed)

    @commands.command(brief='Empty the queue')
    async def empty(self, ctx):
        self.queues[ctx.guild.id] = []

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")


async def setup(bot):
    await bot.add_cog(Music(bot))