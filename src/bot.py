from os import getenv

import discord
from discord.ext import commands

from gadzas_data import GadzasData
from src.bot_cogs import GadzaCog

description = "GadzaBot. Включите всем каналом и наслаждайтесь. Мой префикс - **g!**"
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='g!', description=description, intents=intents)
gadzas_data = GadzasData()


@bot.event
async def on_ready():
    await gadzas_data.update_gadzas_data()


bot.add_cog(GadzaCog(bot, gadzas_data))
bot.run(getenv("BOT_TOKEN"), bot=True)
