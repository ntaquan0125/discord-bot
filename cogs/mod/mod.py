import discord

from discord.ext import commands

class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'{amount} messages deleted.', delete_after=10)
    
    @commands.command(hidden=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} kicked.', delete_after=10)
    
    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} banned.', delete_after=10)

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason=None):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            if user == ban_entry.user:
                await ctx.guild.unban(user, reason=reason)
                await ctx.send(f'{user} unbanned.', delete_after=10)
                return

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        await member.edit(mute=True, reason=reason)
        await ctx.send(f'{member} muted.', delete_after=10)

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        await member.edit(mute=False, reason=reason)
        await ctx.send(f'{member} unmuted.', delete_after=10)

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def deafen(self, ctx, member: discord.Member, *, reason=None):
        await member.edit(deafen=True, reason=reason)
        await ctx.send(f'{member} deafened.', delete_after=10)

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def undeafen(self, ctx, member: discord.Member, *, reason=None):
        await member.edit(deafen=False, reason=reason)
        await ctx.send(f'{member} undeafened.', delete_after=10)
    
    @commands.command(hidden=True)
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nickname):
        await member.edit(nick=nickname)
        await ctx.send(f'{member} renamed to {nickname}.', delete_after=10)


async def setup(bot):
    await bot.add_cog(Moderator(bot))