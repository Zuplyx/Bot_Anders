import asyncio
import datetime

from discord import User
from discord.ext import commands


async def wait(secs: float, author: User, msg: str):
    """
    Waits a specified amount of seconds and then sends a user a message.
    :param secs: seconds to wait
    :param author: user to message
    :param msg: message to send
    """
    await asyncio.sleep(secs)
    await author.send("Here is your reminder for:\n" + msg)


class Time(commands.Cog):
    """
    Init stuff.
    :param bot: Bot to add the cog to
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remindMe(self, ctx: commands.Context, *args):
        """
        Sends the user a reminder.
        :param args:
            To be send a reminder after a certain amount of time use the keyword 'in' followed by the amount of time to
                wait and either 's', 'm', 'h' or 'd' to specify the unit and optionally a message.
            To be send a reminder on a certain date use the keyword 'at' followed by a date in the format 'DD.MM.YYYY HH:mm'
                and optionally a message.
        Examples:
            '!remindMe in 10 s "This is a test".
            '!remindMe at 24.12.2019 12:00 "Time for christmas dinner."
        """
        secs: float
        msg: str
        if args[0] == "in":
            multiplier: int
            if args[2] == "s":  # seconds
                multiplier = 1
            elif args[2] == "m":  # minutes
                multiplier = 60
            elif args[2] == "h":  # hours
                multiplier = 60 * 60
            else:  # days
                multiplier = 60 * 60 * 24
            try:
                secs = int(args[1]) * multiplier
                msg = args[3]
            except TypeError:
                await ctx.send("Error. Could not parse " + args[1])
                return
        else:
            now = datetime.datetime.now()
            try:
                wait_time = datetime.datetime.strptime(args[1], '%d.%m.%Y %H:%M')
                secs = (wait_time - now).total_seconds()
                msg = args[2]
            except (ValueError, UnicodeError) as err:
                await ctx.send("Error:\n" + err)
                return
        asyncio.ensure_future(wait(secs, ctx.author, msg))
        await ctx.author.send("I will send you a reminder when the time is up.")
        return


def setup(bot):  # Adds the web commands to the bot
    bot.add_cog(Time(bot))
