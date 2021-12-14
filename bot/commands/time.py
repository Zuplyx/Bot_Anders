import asyncio
import csv
import datetime

from discord import User
from discord.ext import commands

lock = asyncio.Lock()


async def save_reminder(time: datetime, msg: str, author: User):
    """
    Saves a reminder in a csv file.
    :param time: when the user should be notified
    :param msg: message of the reminder
    :param author: User to remind
    """
    async with lock:
        with open('reminders.csv', mode='a') as reminders_file:
            reminder_writer = csv.writer(reminders_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            reminder_writer.writerow([datetime.datetime.strftime(time, '%d.%m.%Y %H:%M:%S'), msg, author.id])


async def wait(secs: float, author: User, msg: str):
    """
    Waits a specified amount of seconds and then sends a user a message.
    :param secs: seconds to wait
    :param author: user to message
    :param msg: message to send
    """
    await asyncio.sleep(secs)
    now = datetime.datetime.now()
    await author.send("Here is your reminder for:\n>>> " + msg)
    # delete the reminder from the csv file
    lines = []
    async with lock:
        with open('reminders.csv', mode='r+') as reminders_in:
            csv_reader = csv.reader(reminders_in, delimiter=',', quotechar='"')
            for row in csv_reader:
                try:
                    time = datetime.datetime.strptime(row[0], '%d.%m.%Y %H:%M:%S')
                    time_delta = (time - now).total_seconds()
                    # delete the reminder if it is in the past
                    if time_delta < 0:
                        continue
                    lines.append(row)
                except:
                    print("ERROR! Could not delete reminder")
                    continue
        with open('reminders.csv', mode='w') as reminders_out:
            reminder_writer = csv.writer(reminders_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            reminder_writer.writerows(lines)


class Time(commands.Cog):

    def __init__(self, bot):
        """
           Init stuff.
           :param bot: Bot to add the cog to
           """
        self.bot = bot

    @commands.command()
    async def remindMe(self, ctx: commands.Context, *args):
        """
        Sends the user a reminder.
        :param args:
            To be send a reminder after a certain amount of time use the keyword 'in' followed by the amount of time to
                wait and either 's', 'm', 'h' or 'd' to specify the unit and optionally a message.
            To be send a reminder on a certain date use the keyword 'at' followed by a date in the
            format 'DD.MM.YYYY HH:mm' and optionally a message.
        Examples:
            '!remindMe in 10 s "This is a test".
            '!remindMe at 24.12.2019 12:00 "Time for christmas dinner."
        """
        secs: float
        msg: str
        time: datetime
        now = datetime.datetime.now()
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
                time = now + datetime.timedelta(seconds=secs)
                msg = args[3]
            except TypeError:
                await ctx.send("Error. Could not parse " + args[1])
                return
        else:
            try:
                time = datetime.datetime.strptime(args[1], '%d.%m.%Y %H:%M')
                secs = (time - now).total_seconds()
                msg = args[2]
            except (ValueError, UnicodeError) as err:
                await ctx.send("Error:\n" + err)
                return
        asyncio.create_task(save_reminder(time, msg, ctx.author))
        asyncio.create_task(wait(secs, ctx.author, msg))
        await ctx.author.send("I will send you a reminder when the time is up.")
        return

    async def load_reminders(self):
        """
        Creates a reminder for each entry in the 'reminders.csv' file and clears old reminders whose date
        is now in the past.
        """
        async with lock:
            with open('reminders.csv', mode='r+') as reminders_in:
                csv_reader = csv.reader(reminders_in, delimiter=',', quotechar='"')
                lines = []
                time: datetime
                now = datetime.datetime.now()
                for row in csv_reader:
                    try:
                        time = datetime.datetime.strptime(row[0], '%d.%m.%Y %H:%M:%S')
                        # do not load reminders whose date is already in the past
                        if time > now:
                            secs = (time - now).total_seconds()
                            lines.append(row)  # Save it back to the list so we can write it back to the file
                            msg = str(row[1])
                            user: User
                            user_id: int
                            user_id = int(row[2])
                            # try to find the user in the bot's cache
                            user = self.bot.get_user(user_id)
                            if user is None:
                                # make a direct api call if the user was not found in the cache
                                user = await self.bot.fetch_user(user_id)
                            asyncio.create_task(wait(secs, user, msg))
                    except:
                        print("ERROR! Could not load reminder")
            # write all current reminders back to the file
            with open('reminders.csv', mode='w') as reminders_out:
                reminder_writer = csv.writer(reminders_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                reminder_writer.writerows(lines)


def setup(bot):  # Adds the time commands to the bot
    bot.add_cog(Time(bot))
