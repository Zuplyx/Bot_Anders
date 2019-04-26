from random import randint
from typing import Dict

from discord import User
from discord.ext import commands

from minesweeper.GameLogic import Manager


class RussianRoulette(object):
    """
    Represents a game of russian roulette.
    """
    bullet: int
    current: int

    def __init__(self):
        """
        Initializes the game.
        """
        self.current = -1
        self.bullet = randint(0, 5)

    def pull(self) -> bool:
        """
        Pull the trigger.
        :return: revolver discharges ? True : False
        """
        self.current += 1
        if self.current == self.bullet:
            self.__init__()
            return True
        return False


class Games(commands.Cog):
    """
    This contains various games.
    """
    minesweeper_dict: Dict[int, Manager]
    roulette_server_dict: Dict[int, RussianRoulette]

    def __init__(self, bot):
        """
        Just init stuff.
        :param bot: bot to add the cog to
        """
        self.bot = bot
        self.minesweeper_dict = {}
        self.roulette_server_dict = {}

    @commands.command()
    async def minesweeper(self, ctx: commands.Context, *args: str):
        """
        Play a round of minesweeper
        :param ctx: context of the message
        :param args: arguments which are passed to the minesweeper subroutine
        """
        author_hash: int = hash(ctx.author)
        if self.minesweeper_dict.__contains__(author_hash):
            current_manager: Manager = self.minesweeper_dict.get(author_hash)
        else:
            current_manager = Manager()
            self.minesweeper_dict[author_hash] = current_manager
        result: str = "```" + current_manager.parse_input(" ".join(args)) + "```"
        await ctx.send(result)

    @commands.command()
    async def roulette(self, ctx: commands.Context, arg):
        """
        Play russian roulette.
        Use 'new' to start a new round.
        :param ctx: context of message
        :param arg: 'new' to start a new round or '' to pull the trigger
        :return: The result of the game.
        """
        server_hash: int = hash(ctx.guild)
        if arg == "new" or not self.roulette_server_dict.__contains__(server_hash):
            self.roulette_server_dict[server_hash] = RussianRoulette()
        else:
            author: User = ctx.author
            message: str = "The trigger is pulled and " + author.mention
            roulette: RussianRoulette = self.roulette_server_dict.get(server_hash)
            if roulette.pull():
                message += " is killed!."
            else:
                message *= " lives!"
            await ctx.send(message)


def setup(bot):
    bot.add_cog(Games(bot))
    # Adds the games commands to the bot
