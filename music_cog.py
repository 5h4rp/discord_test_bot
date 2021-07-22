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
        self.is_playing = False
        self.queue = []

    @staticmethod
    async def is_joined(voice, author_voice):
        action = 'invalid'
        if author_voice and voice and voice.is_connected():
            action = 'move'
        elif author_voice:
            action = 'join'

        return action

    @commands.command()
    async def join(self, ctx, action=None):
        print(action)
        print('join invoked!')
        author_voice = ctx.message.author.voice
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        action = MusicCog.is_joined(voice, author_voice) if action is None or action not in ('move', 'join') else action
        if action == 'move':
            await voice.move_to(author_voice.channel)
        elif action == 'join':
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
            # print(info['title'])
            ydl_title = info['title']
            ydl_url = info['url']
        return ydl_title, ydl_url

    # async def play_next(self):
    #     if len(self.queue) > 0:
    #         self.is_playing = True
    #
    #         # get the first url
    #         m_url = self.queue[0][0]['source']
    #
    #         # remove the first element as you are currently playing it
    #         self.queue.pop(0)
    #
    #         self.bot.voice_clients.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS), after=lambda e: self.play_next())
    #     else:
    #         self.is_playing = False

    # async def play_music(self):
    #     if len(self.queue) > 0:
    #         self.is_playing = True
    #
    #         m_url = self.queue[0][0]['source']
    #
    #         # try to connect to voice channel if you are not already connected
    #         voice, author_voice, action = self.is_joined()
    #
    #         print(self.queue)
    #         # remove the first element as you are currently playing it
    #         self.queue.pop(0)
    #
    #         self.vc.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS), after=lambda e: self.play_next())
    #     else:
    #         self.is_playing = False

    @commands.command(name='play')
    async def play_command(self, ctx, *, url_or_search):
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
            self.queue = list()
            voice.stop()
            await ctx.send('Stopping...')
