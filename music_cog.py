import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

from youtube_dl import YoutubeDL


YDL_OPTIONS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


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
        self.queue = []

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

    @staticmethod
    def get_ydl_url(url_or_search):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url_or_search, download=False)
        if "_type" in info and info["_type"] == "playlist":
            return MusicCog.get_ydl_url(info["entries"][0]["url"])
        else:
            ydl_url = info['url']
        return ydl_url

    @commands.command()
    async def play(self, ctx, *, url_or_search):
        print('play invoked!')
        # url_or_search = ' '.join(url_or_search)
        print(url_or_search)

        author_voice = ctx.message.author.voice
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if author_voice and (not voice or not voice.is_connected()):
            await self.join(ctx)

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            ydl_url = MusicCog.get_ydl_url(url_or_search)
            print(ydl_url)
            voice.play(FFmpegPCMAudio(ydl_url, **FFMPEG_OPTIONS), after=lambda e: print('finished playing'))
            print(voice.is_playing())
            await ctx.send('Bot is playing')
        else:
            self.queue.append(url_or_search)

    @commands.command()
    async def stop(self, ctx):
        print('stop invoked!')
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.send('Stopping...')
