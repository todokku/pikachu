import discord
import os
import time
from configs import config
from discord.ext import commands

bot = commands.Bot(
    command_prefix=config.COMMAND_PREFIX,
    help_command=None
)

extensions = [
    "cogs.alert",
    "cogs.dice",
    "cogs.level"
]

TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    os.environ["TZ"] = "US/Eastern"
    # os.environ["TZ"] = "US/Central"
    time.tzset()

    now = time.strftime("%H:%M")
    status = discord.Streaming(name="{} in ToW".format(now), url="https://twitch.tv/topic8")
    await bot.change_presence(status=discord.Status.online, activity=status)

    for extension in extensions:
        bot.load_extension(extension)

@bot.event
async def on_member_join(member):
    if member.guild == bot.get_guild(config.GUILD_ID):
        await member.create_dm()
        await member.dm_channel.send(file=discord.File('pikachu-sqlite/assets/images/op-1.png'))
        await member.dm_channel.send(file=discord.File('pikachu-sqlite/assets/images/op-2.png'))
        await member.dm_channel.send(file=discord.File('pikachu-sqlite/assets/images/op-3.png'))
        await member.dm_channel.send(file=discord.File('pikachu-sqlite/assets/images/op-4.png'))
        await member.dm_channel.send(file=discord.File('pikachu-sqlite/assets/images/op-5.png'))

if __name__ == "__main__":
    bot.run(TOKEN, bot=True, reconnect=True)