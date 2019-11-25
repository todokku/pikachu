import os
import sqlite3
from configs import config
from discord.ext import commands
from sqlite3 import Error

class Level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
        try:
            cwd = os.path.abspath(os.getcwd())
            db = os.path.join(cwd, config.db_name + ".db")
            self.db = sqlite3.connect(db)
            self.db_cursor = self.db.cursor()

            self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, level INTEGER, exp INTEGER)
            """)

        except Error as e:
            print(e)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content.startswith(config.command_prefix):
            return

        self.db_cursor.execute("SELECT * FROM users WHERE id = ?",[message.author.id])
        response = self.db_cursor.fetchone()

        if not response:
            self.db_cursor.execute("INSERT INTO users VALUES (?, ?, ?)", [message.author.id, 1, 0])
            self.db.commit()

        user_id, user_level, user_exp = response
        user_exp += config.exp_gained
        old_level = user_level
        user_level = int(user_exp / config.exp_leveled) + 1
        
        if user_level > old_level:
            await message.channel.send("<@{}> has leveled up to {}!".format(user_id, user_level))

        self.db_cursor.execute("UPDATE users SET level = ?, exp = ? WHERE id = ?",
            [user_level, user_exp, message.author.id])
        self.db.commit()

    @commands.command(aliases=["profile"])
    async def profile_command(self, ctx):
        self.db_cursor.execute("SELECT * FROM users WHERE id = ?", [ctx.author.id])
        response = self.db_cursor.fetchone()

        if not response:
            return

        user_id, user_level, user_exp = response

        await ctx.send("<@{}>, you are level {}!".format(user_id, user_level, user_exp))

def setup(bot):
    bot.add_cog(Level(bot))