import discord
from discord.ext import commands
from os import getenv
from cogs import GadzaCog
from gadzas_data import GadzasData

description = "GadzaBot. Включите всем каналом и наслаждайтесь. Мой префикс - **g!**"
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='g!', description=description, intents=intents)
gadzas_data = GadzasData()

bot.add_cog(GadzaCog(bot, gadzas_data))
bot.run(getenv("BOT_TOKEN"), bot=True)
