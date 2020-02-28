import discord
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
            self.db_cursor.execute("INSERT INTO bot.users VALUES (%s,%s,%s);", [str(message.author.id), 1, 0])
            self.db.commit()
            self.db_cursor.execute("SELECT * FROM bot.users WHERE id=%s;", [str(message.author.id)])
            response = self.db_cursor.fetchone()

        user_id, user_level, user_exp = response
        user_exp += config.EXP_GAINED_PER_MSG
        next_level_exp = (config.EXP_GAINED_PER_MSG * (user_level+1) ** 2 - config.EXP_GAINED_PER_MSG * (user_level+1))
        
        if user_exp >= next_level_exp:
            user_level += 1
            await message.channel.send("<@{}> has leveled up to {}!".format(user_id, user_level))

        self.db_cursor.execute("UPDATE bot.users SET level=%s, exp=%s WHERE id=%s;",
            [user_level, user_exp, str(message.author.id)])
        self.db.commit()

    @commands.command(aliases=["profile"])
    async def profile_command(self, ctx):
        self.db_cursor.execute("SELECT * FROM bot.users WHERE id=%s;", [str(ctx.author.id)])
        response = self.db_cursor.fetchone()

        if not response:
            return

        user_id, user_level, user_exp = response
        next_level_exp = (config.EXP_GAINED_PER_MSG * (user_level+1) ** 2 - config.EXP_GAINED_PER_MSG * (user_level+1))

        await ctx.send("<@{}>, you are level {}[{}/{}]!".format(user_id, user_level, user_exp, next_level_exp))

    @commands.command(aliases=["giveexp"])
    async def giveexp_command(self, ctx, *args):
        if not ctx.author.id in config.OWNER_IDS:
            return

        if not ctx.message.mentions:
            return

        if len(args) >= 2:
            users = [user for user in ctx.message.mentions]

            for user in users:
                self.db_cursor.execute("SELECT * FROM bot.users WHERE id=%s;", [str(user.id)])
                response = self.db_cursor.fetchone()

                if not response:
                    return

                user_id, user_level, user_exp = response

                user_exp += int(args[1])

                while True:
                    next_level_exp = (config.EXP_GAINED_PER_MSG * (user_level+1) ** 2 - config.EXP_GAINED_PER_MSG * (user_level+1))

                    if next_level_exp > user_exp:
                        break

                    user_level += 1

                self.db_cursor.execute("UPDATE bot.users SET level=%s, exp=%s WHERE id=%s;", [user_level, user_exp, str(user.id)])
                self.db.commit()

            await ctx.send("Exp has been given out.")

    @commands.command(aliases=["ranking"])
    async def ranking_command(self, ctx):
        self.db_cursor.execute("SELECT * FROM bot.users WHERE id!=%s ORDER BY exp DESC LIMIT 15;", [str(config.OWNER_IDS)])
        response = self.db_cursor.fetchmany(15)

        embed = discord.Embed(
            title="Top 15 Ranking",
            color=0xffff00
        )

        if not response:
            return

        for res in response:
            user_id, user_level, user_exp = res
            user = await self.bot.fetch_user(user_id)

            embed.add_field(
                name="{}#{}".format(user.name, user.discriminator),
                value="Level {}".format(user_level),
                inline=True
            )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Level(bot))