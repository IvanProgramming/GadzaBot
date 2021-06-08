import discord
from discord.ext import commands

from gadzas_data import GadzasData
from src.bot_cogs import GadzaCog
from src.settings import BOT_TOKEN, IS_BOT, GADZAS_DATA_NETWORK, GADZAS_DATA_PATH

description = "GadzaBot. Включите всем каналом и наслаждайтесь. Мой префикс - g!"
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='g!', description=description, intents=intents)
gadzas_data = GadzasData(is_offline=GADZAS_DATA_NETWORK, gadzas_offline_path=GADZAS_DATA_PATH)


@bot.event
async def on_ready():
    await gadzas_data.update_gadzas_data()


bot.add_cog(GadzaCog(bot, gadzas_data))
bot.run(BOT_TOKEN, bot=IS_BOT)
