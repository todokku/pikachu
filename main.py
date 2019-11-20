from discord.ext import commands
from os import getenv

bot = commands.Bot(
    command_prefix="!",
    help_command=None,
    owner_ids=[138491187370786816]
)

extensions = [
    "cogs.games"
]

token = getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    for extension in extensions:
        bot.load_extension(extension)

if __name__ == "__main__":
    bot.run(token, bot=True, reconnect=True)