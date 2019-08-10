from random import choice, randint

from discord.ext import commands


class Random(commands.Cog):
    """
    This contains various random choice commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coin(self, ctx: commands.Context):
        """
        Flips a coin.
        :return: 'Heads' or 'Tails'
        """
        await ctx.send(choice(["Heads", "Tails"]))

    @commands.command()
    async def dice(self, ctx: commands.Context):
        """
        Rolls a dice.
        :return: 1-6
        """
        await ctx.send("You rolled " + str(randint(1, 6)) + ".")


def setup(bot):
    bot.add_cog(Random(bot))
    # Adds the random commands to the bot
