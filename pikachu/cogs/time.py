from datetime import datetime
from discord.ext import commands

class Time(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["age"])
    async def age_command(self, ctx):
        now = datetime.now()
        start = ctx.author.created_at
        duration = (now-start).total_seconds()

        years = divmod(duration, 31536000)
        days = divmod(years[1] if years[1] != None else duration, 86400)
        hours = divmod(days[1] if days[1] != None else duration, 3600)
        minutes = divmod(hours[1] if hours[1] != None else duration, 60)
        seconds = divmod(minutes[1], 1) if minutes[1] is not None else duration

        years = int(years[0])
        days = int(days[0])
        hours = int(hours[0])
        minutes = int(minutes[0])
        seconds = int(seconds[0])

        response = "you are "

        if years:
            response += "{} years, ".format(years) if years > 1 else "{} year, ".format(years)

        if days:
            response += "{} days, ".format(days) if days > 1 else "{} day, ".format(days)

        if hours:
            response += "{} hours, ".format(hours) if hours > 1 else "{} hour, ".format(hours)

        if minutes:
            response += "{} minutes, ".format(minutes) if minutes > 1 else "{} minute, ".format(minutes)

        if seconds:
            response += "{} seconds ".format(seconds) if seconds > 1 else "{} second ".format(seconds)

        await ctx.send("<@{}>, {}".format(ctx.author.id, response + "old."))

def setup(bot):
    bot.add_cog(Time(bot))