import discord
import os
import psycopg2
import time
from configs import config
from discord.ext import commands, tasks

class Alert(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.db = psycopg2.connect(config.DATABASE_URL, sslmode="require")
        self.db_cursor = self.db.cursor()

        self.db_cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS bot;
        CREATE TABLE IF NOT EXISTS bot.events (
            id SERIAL,
            message TEXT NOT NULL,
            days TEXT NOT NULL,
            time TEXT NOT NULL
        );
        """)

        self.update.start()

    @tasks.loop(seconds=1.0)
    async def update(self):
        channel = self.bot.get_channel(config.CHANNEL_ID)
        role = config.ROLE_ID
        day = time.strftime("%a")
        now = time.strftime("%H:%M")
        second = time.strftime("%S")

        if second == "00":
            status = discord.Streaming(name="{} in ToW".format(now), url="https://twitch.tv/topic8")
            await self.bot.change_presence(status=discord.Status.online, activity=status)

        self.db_cursor.execute("SELECT * FROM bot.events WHERE time=%s", [now])
        response = self.db_cursor.fetchall()

        if not response:
            return

        events = [event for event in response]

        for event in events:
            message = event[1]
            days = list(map(str, event[2].split(",")))

            if day in days and second == "00":
                await channel.send("<@&{}> {}".format(role, message))

    @commands.command(aliases=["addevent"])
    async def addevent_command(self, ctx, *args):
        if not ctx.author.id in config.OWNER_IDS:
            return

        if len(args) == 3:
            message, days, time = args
            self.db_cursor.execute("INSERT INTO bot.events (message, days, time) VALUES (%s,%s,%s)",
                [message, days, time])
            self.db.commit()
            await ctx.send("Your event has been added.")

    @update.before_loop
    async def before_update(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Alert(bot))