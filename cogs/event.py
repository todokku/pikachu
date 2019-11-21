import discord
import os
import sqlite3
import time
from configs import config
from discord.ext import commands
from sqlite3 import Error

class Event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        try:
            cwd = os.path.abspath(os.getcwd())
            db = os.path.join(cwd, config.db_name + ".db")
            self.db = sqlite3.connect(db)
            self.db_cursor = self.db.cursor()

            self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, gid INTEGER, name TEXT, day TEXT, time TEXT)
            """)

        except Error as e:
            print(e)

def setup(bot):
    bot.add_cog(Event(bot))
