import discord
from discord.ext import commands
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

for file in os.listdir("commands"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"commands.{name}")


@bot.command()
async def nice(ctx):
    await ctx.send('Nice!')

bot.run(DISCORD_TOKEN)
