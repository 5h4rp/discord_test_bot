# bot.py
import os
import random

import discord
from discord.ext import commands

from dotenv import load_dotenv

from music_cog import MusicCog
from misc_cog import MiscCog

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.playing, name='with code')
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)

bot.add_cog(MusicCog(bot))
bot.add_cog(MiscCog(bot))


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    # guild = discord.utils.get(bot.guilds, name=GUILD)

    # print(
    #     f'{client.user} is connected to the following guild:\n'
    #     f'{guild.name}(id: {guild.id})'
    # )

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

    # owner = guild.owner
    # print(owner)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        await ctx.send(error)
        # print(error)
        # raise error


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
