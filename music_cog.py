import discord
from discord.ext import commands

from youtube_dl import YoutubeDL


async def in_voice_channel(ctx):
    voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client
    if voice and bot_voice and voice.channel and bot_voice.channel and voice.channel == bot_voice.channel:
        return True
    else:
        raise commands.CommandError("You need to be in the channel to do that.")


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        print('join invoked!')
        author_voice = ctx.message.author.voice
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if author_voice and voice and voice.is_connected():
            await voice.move_to(author_voice.channel)
        elif author_voice:
            await author_voice.channel.connect()
        else:
            await ctx.send('User not connected to any voice channel')

    @commands.command()
    @commands.check(in_voice_channel)
    async def leave(self, ctx):
        print('leave invoked!')
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send('Not connected to voice channel')

