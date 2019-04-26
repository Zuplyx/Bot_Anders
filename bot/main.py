from discord import Message, TextChannel
from discord.ext import commands

from minesweeper.GameLogic import send_help

# global variables
with open("discord_token.txt") as token_file:
    token = token_file.readline()
description: str = " A simple bot with a variety of commands."
bot_anders = commands.Bot(command_prefix='!', description=description, pm_help=True)
cogs = ['commands.games', 'commands.random']


@bot_anders.event
async def on_message(message: Message):
    if message.author.bot:
        return  # do not react on messages from the bot itself
    if message.content == "!help minesweeper":
        channel: TextChannel = message.channel
        await channel.send("```" + send_help() + "```")
        return
    await bot_anders.process_commands(message)


@bot_anders.event
async def on_ready():
    print(f'Logged in as {bot_anders.user.name} - {bot_anders.user.id}')
    for cog in cogs:
        bot_anders.load_extension(cog)


bot_anders.run(token)
