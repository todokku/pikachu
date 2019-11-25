import discord
import os
from configs import config
from discord.ext import commands

bot = commands.Bot(
    command_prefix=config.command_prefix,
    help_command=None
)

extensions = [
    "cogs.dice",
    "cogs.event",
    "cogs.level"
]

token = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    for extension in extensions:
        bot.load_extension(extension)

@bot.event
async def on_member_join(member):
    if member.guild == bot.get_guild(config.guild_id):
        await member.create_dm()
        await member.dm_channel.send(file=discord.File('assets/images/op-1.png'))
        await member.dm_channel.send(file=discord.File('assets/images/op-2.png'))
        await member.dm_channel.send(file=discord.File('assets/images/op-3.png'))
        await member.dm_channel.send(file=discord.File('assets/images/op-4.png'))
        await member.dm_channel.send(file=discord.File('assets/images/op-5.png'))

if __name__ == "__main__":
    bot.run(token, bot=True, reconnect=True)