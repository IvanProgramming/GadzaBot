from discord.ext import commands

from gadzas_data import GadzasData
from src.bot_cogs import GadzaCog, SettingsCog
from src.settings import BOT_TOKEN, IS_BOT, GADZAS_DATA_NETWORK, GADZAS_DATA_PATH

bot = commands.Bot(command_prefix=SettingsCog.get_prefix)
gadzas_data = GadzasData(is_offline=GADZAS_DATA_NETWORK, gadzas_offline_path=GADZAS_DATA_PATH)
bot.add_cog(GadzaCog(bot, gadzas_data))
bot.add_cog(SettingsCog(bot))
bot.run(BOT_TOKEN, bot=IS_BOT)
