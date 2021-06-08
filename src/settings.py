# This is configuration file. Instead of this you can use configuration via enviroment variables,
# in this way, just don't touch this file. If you choose configuration via this file, replace os.getenv("{KEY}) to your
# value in quotes. Also don't forget to replace this file, if you will load you project to GitHub or another public place

import os

# Discord Bot Token. Visit discord.com/developers to get this one (can be obtained in Bot tab)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# discord.py library can also give you access with user token,in this case you should change this flag to False
IS_BOT = True

# Path to all Gadza mediafiles
GADZAS_PATH = "./res/gadzas"

# Network gadzasData. If you want to use local copy of it, please, change to False
GADZAS_DATA_NETWORK = True

# Only if GADZAS_NETWORK is False. Set here path to gadzasData file
GADZAS_DATA_PATH = ""

# DB url. More information here - https://tortoise-orm.readthedocs.io/en/latest/databases.html?highlight=url#db-url
DB_URL = os.getenv("DB_URL")
