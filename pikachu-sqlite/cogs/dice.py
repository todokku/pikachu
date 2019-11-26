import random
from discord.ext import commands

class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["roll", "r"])
    async def roll_command(self, ctx, *args):
        if len(args) == 0:
            number_of_dice = 4
            number_of_sides = 6
            dice = [str(random.choice(range(1, number_of_sides + 1))) for d in range(number_of_dice)]
            await ctx.send(", ".join(dice) + ". You rolled a **{}**!".format(sum(int(d) for d in dice)))

def setup(bot):
    bot.add_cog(Dice(bot))