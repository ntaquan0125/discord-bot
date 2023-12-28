import asyncio
import random
import discord
import yt_dlp as youtube_dl

from typing import Union
from discord.ext import commands


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
    'source_address': '0.0.0.0',  # Bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.thumbnail = data.get('thumbnail')
        self.requester = ''

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # Take the first item from a playlist
            data = data['entries'][0]
    
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    @staticmethod
    def parse_duration(duration):
        if duration > 0:
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)

            duration = []
            if days > 0:
                duration.append(str(days))
            if hours > 0:
                duration.append(str(hours))
            if minutes > 0:
                duration.append(str(minutes))
            if seconds > 0:
                duration.append(str(seconds))
            value = ':'.join(duration)

        elif duration == 0:
            value = "LIVE"

        return value


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    @commands.command()
    async def join(self, ctx, *, channel: Union[discord.VoiceChannel, None]):
        if channel is None and ctx.author.voice:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        source = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        source.requester = ctx.author

        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []
        self.queues[ctx.guild.id].append(source)
        await ctx.send(f'`{source.title}` has been added to queue.')

        await self.play_from_queue(ctx)

    async def play_from_queue(self, ctx):
        if not ctx.voice_client.is_playing():
            if len(self.queues[ctx.guild.id]) > 0:
                source = self.queues[ctx.guild.id].pop(0)
                ctx.voice_client.play(source,
                    after=lambda e: asyncio.run_coroutine_threadsafe(
                        self.play_from_queue(ctx), self.bot.loop
                        )
                    )

                embed = discord.Embed(
                    title='Now playing',
                    description=f'```{source.title}```',
                    colour=discord.Color.random()
                )
                embed.add_field(name='Duration', value=source.duration)
                embed.add_field(name='Requested by', value=source.requester.name)
                embed.set_thumbnail(url=source.thumbnail)
                await ctx.send(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('Audio is paused.')
        else:
            await ctx.send('Currently no audio is playing.')

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('Resumed audio.')
        else:
            await ctx.send('The audio is not paused.')

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send('Not connected to a voice channel.')
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f'Changed volume to {volume}%.')

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        await self.play_from_queue(ctx)

    @commands.command()
    async def queue(self, ctx):
        if len(self.queues[ctx.guild.id]) == 0:
            await ctx.send('The queue is currently empty.')
        else:
            description = []
            for i, song in enumerate(self.queues[ctx.guild.id]):
                description += f'{i+1}. {song.title}\n'

            embed = discord.Embed(
                title='Song Queue',
                description=''.join(description),
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def shuffle(self, ctx):
        if len(self.queues[ctx.guild.id]) == 0:
            await ctx.send('The queue is currently empty.')
        else:
            random.shuffle(self.queues[ctx.guild.id])
            description = []
            for i, song in enumerate(self.queues[ctx.guild.id]):
                description += f'{i+1}. {song.title}\n'

            embed = discord.Embed(
                title='Song Queue',
                description=''.join(description),
                colour=discord.Color.random()
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def empty(self, ctx):
        self.queues[ctx.guild.id] = []

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('You are not connected to a voice channel.')
                raise commands.CommandError('Author not connected to a voice channel.')


async def setup(bot):
    await bot.add_cog(Music(bot))