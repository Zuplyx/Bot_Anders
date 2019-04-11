from typing import Dict

from discord.ext import commands

from minesweeper.GameLogic import Manager

# global variables
with open("discord_token.txt") as token_file:
    token = token_file.readline()
bot_anders = commands.Bot(command_prefix='!')
minesweeper_dict: Dict[int, Manager] = {}


@bot_anders.command()
async def minesweeper(ctx: commands.Context, *args: str):
    """
    Command to play minesweeper
    :param ctx: context of the message
    :param args: arguments which are passed to the minesweeper subroutine
    """
    author_hash: int = hash(ctx.author)
    if minesweeper_dict.__contains__(author_hash):
        current_manager: Manager = minesweeper_dict.get(author_hash)
    else:
        current_manager = Manager()
        minesweeper_dict[author_hash] = current_manager
    result: str = current_manager.parse_input(" ".join(args))
    print(result)
    print(minesweeper_dict)
    await ctx.send(result)


bot_anders.run(token)
