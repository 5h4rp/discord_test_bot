# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.all()

activity = discord.Activity(type=discord.ActivityType.playing, name='with code')
client = discord.Client(intents=intents, activity=activity)

@client.event
async def on_ready():
    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    owner = guild.owner
    print(owner)

client.run(TOKEN)