from random import randint
from typing import Dict

from discord import User, DMChannel, GroupChannel
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
        if self.current == self.bullet:  # the trigger was pulled and the game is reset
            self.__init__()
            return True
        return False


class Games(commands.Cog):
    """
    This contains various games.
    """
    minesweeper_dict: Dict[int, Manager]
    roulette_server_dict: Dict[int, RussianRoulette]
    roulette_group_dict: Dict[int, RussianRoulette]

    def __init__(self, bot):
        """
        Just init stuff.
        :param bot: bot to add the cog to
        """
        self.bot = bot
        self.minesweeper_dict = {}
        self.roulette_server_dict = {}
        self.roulette_group_dict = {}

    @commands.command()
    async def minesweeper(self, ctx: commands.Context, *args: str):
        """
        Play a round of minesweeper
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

    @staticmethod
    def start_new_round() -> (str, RussianRoulette):
        return "Created a new round of russian roulette. Use !roulette to play.", RussianRoulette()

    @commands.command()
    async def roulette(self, ctx: commands.Context, *args):
        """
        Play russian roulette.
        Use 'new' to start a new round.
        :param args: 'new' to start a new round or nothing to pull the trigger
        :return: The result of the game.
        """
        if isinstance(ctx.channel, DMChannel):
            await ctx.send("Roulette can only be played on servers or in group chats.")
            return
        group: bool = isinstance(ctx.channel, GroupChannel)
        hash_code: int = hash(ctx.channel)
        if args.__contains__("new") or (group and not self.roulette_group_dict.__contains__(hash_code)) \
                or (not group and not self.roulette_server_dict.__contains__(hash_code)):
            # We have to start a new round.
            new_round: (str, RussianRoulette) = Games.start_new_round()
            await ctx.send(new_round[0])
            if group:
                self.roulette_group_dict[hash_code] = new_round[1]
            else:
                self.roulette_server_dict[hash_code] = new_round[1]
            return
        else:
            if group:
                roulette: RussianRoulette = self.roulette_group_dict.get(hash_code)
            else:
                roulette: RussianRoulette = self.roulette_server_dict.get(hash_code)
        author: User = ctx.author
        message: str = "The trigger is pulled and " + author.mention
        if roulette.pull():
            message += " is killed!"
        else:
            message += " lives!"
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Games(bot))
    # Adds the games commands to the bot
