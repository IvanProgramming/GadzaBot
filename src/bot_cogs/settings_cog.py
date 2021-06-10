from typing import Dict

import discord
from discord.ext import commands

from src.exceptions.administration_exceptions import PrefixTooLong
from src.info_embeds import PrefixSetSuccessful
from src.models import Guild, init_database
from src.settings import SAFE_MODE_DB

prefixes_dict: Dict[int, str] = {}


class SettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_prefix(bot: commands.Bot, message: discord.Message):
        """ Prefix function to get server's own prefix """
        global prefixes_dict
        if message.guild.id in prefixes_dict:
            return prefixes_dict[message.guild.id]
        else:
            prefix = await Guild.get_prefix(message.guild.id)
            prefixes_dict[message.guild.id] = prefix
            return prefix

    @commands.command(name="set_prefix", aliases=["prefix", "sp", "префикс"])
    async def set_prefix(self, ctx: commands.Context, new_prefix: str):
        global prefixes_dict
        required_guild = await Guild.filter(id=ctx.guild.id).first()
        try:
            await required_guild.change_prefix(new_prefix)
            prefixes_dict[ctx.guild.id] = new_prefix
        except PrefixTooLong as e:
            await ctx.send(embed=e.to_embed())
        else:
            await ctx.send(embed=PrefixSetSuccessful(new_prefix).as_embed())

    @commands.Cog.listener()
    async def on_ready(self):
        await init_database(safe=SAFE_MODE_DB)
        for guild in self.bot.guilds:
            await Guild.add_server(guild.id)
