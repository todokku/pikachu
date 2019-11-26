import os
import psycopg2
from configs import config
from discord.ext import commands

class Level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        DATABASE_URL = os.getenv("DATABASE_URL")
        
        self.db = psycopg2.connect(DATABASE_URL, sslmode="require")
        self.db_cursor = self.db.cursor()
        self.db_cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS bot;
        CREATE TABLE IF NOT EXISTS bot.users (
            id TEXT PRIMARY KEY,
            level INTEGER NOT NULL,
            exp INTEGER NOT NULL
        );
        """)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content.startswith(config.COMMAND_PREFIX):
            return

        self.db_cursor.execute("SELECT * FROM bot.users WHERE id=%s;", [str(message.author.id)])
        response = self.db_cursor.fetchone()

        if not response:
            self.db_cursor.execute("INSERT INTO bot.users VALUES (%s,%s,%s)", [str(message.author.id), 1, 0])
            self.db.commit()

        user_id, user_level, user_exp = response
        user_exp += config.EXP_GAINED_PER_MSG
        old_level = user_level
        user_level = int(user_exp / config.EXP_NEEDED_PER_LEVEL) + 1
        
        if user_level > old_level:
            await message.channel.send("<@{}> has leveled up to {}!".format(user_id, user_level))

        self.db_cursor.execute("UPDATE bot.users SET level=%s, exp=%s WHERE id=%s",
            [user_level, user_exp, str(message.author.id)])
        self.db.commit()

    @commands.command(aliases=["profile"])
    async def profile_command(self, ctx):
        self.db_cursor.execute("SELECT * FROM bot.users WHERE id=%s", [str(ctx.author.id)])
        response = self.db_cursor.fetchone()

        if not response:
            return

        user_id, user_level, user_exp = response

        await ctx.send("<@{}>, you are level {}!".format(user_id, user_level))

def setup(bot):
    bot.add_cog(Level(bot))