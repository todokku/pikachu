import discord
import os
import sqlite3
import time
from configs import config
from discord.ext import commands, tasks
from sqlite3 import Error

class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        os.environ["TZ"] = "US/Eastern"
        # os.environ["TZ"] = "US/Central"
        time.tzset()

        try:
            cwd = os.path.abspath(os.getcwd())
            db = os.path.join(cwd, config.db_name + ".db")
            self.db = sqlite3.connect(db)
            self.db_cursor = self.db.cursor()

            self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, days TEXT, time TEXT)
            """)

            self.send_alert.start()
            self.update_status.start()

        except Error as e:
            print(e)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild == self.bot.get_guild(config.guild_id):
            await member.create_dm()
            await member.dm_channel.send(file=discord.File('assets/images/op-1.png'))
            await member.dm_channel.send(file=discord.File('assets/images/op-2.png'))
            await member.dm_channel.send(file=discord.File('assets/images/op-3.png'))
            await member.dm_channel.send(file=discord.File('assets/images/op-4.png'))
            await member.dm_channel.send(file=discord.File('assets/images/op-5.png'))

    @tasks.loop(seconds=1.0)
    async def send_alert(self):
        channel = self.bot.get_channel(config.channel_id)
        role = config.role_id
        day = time.strftime("%a")
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        now = hour + ":" + minute

        self.db_cursor.execute("SELECT * FROM events WHERE time = ?", [now])
        response = self.db_cursor.fetchall()

        if not response:
            return

        events = [event for event in response]

        for event in events:
            message = event[1]
            days = list(map(str, event[2].split(",")))

            if day in days and second == "00":
                await channel.send("<@&{}> {}".format(role, message))

    @tasks.loop(seconds=10.0)
    async def update_status(self):
        hour = time.strftime("%H")
        minute = time.strftime("%M")

        status = discord.Streaming(name="{}:{} in ToW".format(hour, minute), url="https://twitch.tv/topic8")
        await self.bot.change_presence(status=discord.Status.online, activity=status)

    @commands.command(aliases=["addevent"])
    async def addevent_command(self, ctx, *args):
        if len(args) == 3:
            message, days, time = args
            self.db_cursor.execute("INSERT INTO events (message, days, time) VALUES (?, ?, ?)", [message, days, time])
            self.db.commit()
            await ctx.send("Your event has been added.")

    @send_alert.before_loop
    async def before_send_alert(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Event(bot))