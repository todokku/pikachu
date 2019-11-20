import discord
import os
from configs import config
from discord.ext import commands

bot = commands.Bot(
    command_prefix=config.command_prefix,
    help_command=None,
    owner_ids=config.owner_ids
)

token = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    status = discord.Game(name="DDU-DU DDU-DU")
    await bot.change_presence(status=discord.Status.online, activity=status)

    for extension in config.extensions:
        bot.load_extension(extension)

if __name__ == "__main__":
    bot.run(token, bot=True, reconnect=True)