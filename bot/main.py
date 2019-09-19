from sys import exit
from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

from discord import Message, TextChannel
from discord.ext import commands

from minesweeper.GameLogic import send_help

# global variables
with open("discord_token.txt") as token_file:
    token = token_file.readline()  # get the token
description: str = " A simple bot with a variety of commands."
bot_anders = commands.Bot(command_prefix='!', description=description)
cogs = ['commands.games', 'commands.random', 'commands.web', 'commands.time']


@bot_anders.event
async def on_message(message: Message):
    if message.author.bot:
        return  # do not react on messages from the bot itself
    if message.content == "!help minesweeper":
        channel: TextChannel = message.channel
        await channel.send("```" + send_help() + "```")
        return
    if message.content == "!help poll":
        channel: TextChannel = message.channel
        await channel.send("```" + "!poll ARGS\n\nARGS: Arguments from which the poll is created. The first argument "
                                   "is the title, all other arguments are the options.\nNote: Multi-word arguments "
                                   "have to be quoted.\nExample: !poll \"Is this command great?\" Yes No" + "```")

        return
    await bot_anders.process_commands(message)


@bot_anders.event
async def on_ready():
    print(f'Logged in as {bot_anders.user.name} - {bot_anders.user.id}')
    for cog in cogs:
        bot_anders.load_extension(cog)


# check if the network is already connected
loop_value = True
tries = 0
while loop_value:
    try:
        urlopen("http://google.com")
        loop_value = False
    except URLError as e:
        tries += 1
        print(e.reason)
        if tries < 11:
            print("Retrying in 5 seconds.")
        else:
            print("No internet connection available after 10 tries. The program will now terminate.")
            exit(1)
    sleep(5)
else:
    bot_anders.run(token)
