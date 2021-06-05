from os import getenv

import discord
from discord.ext import commands

from exceptions import UserIsNotConnectedError, PermissionConnectError, PermissionSpeakError
from gadzas_data import GadzasData
from src.exceptions import BaseDiscordException

description = "GadzaBot. Включите всем каналом и наслаждайтесь. Мой префикс - **g!**"
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='g!', description=description, intents=intents)
gadzas_data = GadzasData()

@bot.event
async def on_ready():
    await gadzas_data.update_gadzas_data()
    print(gadzas_data.dict)
    print(gadzas_data.all)


class GadzaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx: commands.Context):
        gadza_key = gadzas_data.random().gadza_key
        await self.play(gadza_key, ctx.voice_client)

    @random.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        try:
            channel = await self.get_user_channel(ctx.author)
            await self.connect(channel)
        except BaseDiscordException as e:
            await ctx.send(embed=e.to_embed())

    async def connect(self, channel: discord.VoiceChannel):
        """ Connects user to channel, also checking permissions and supress ClientException
        :param channel: Channel to connect
        :raises PermissionConnectError bot doesn't have permissions for connecting channel
        :raises PermissionSpeakError bot doesn't have permissions to speak in channel
        """
        bot_as_member = await channel.guild.fetch_member(bot.user.id)
        if not channel.permissions_for(bot_as_member).connect:
            raise PermissionConnectError
        else:
            try:
                await channel.connect()
                if not channel.permissions_for(bot_as_member).speak:
                    raise PermissionSpeakError
            except discord.ClientException:
                pass

    @staticmethod
    async def get_user_channel(member: discord.Member) -> discord.VoiceChannel:
        """ Returns voice channel of user
            :param member Member object of connected user
            :returns VoiceChannel object. This is VoiceChannel, that user is connected
            :raises UserIsNotConnectedError if user is not connected to any voice channel
        """
        if member.voice:
            return member.voice.channel
        else:
            raise UserIsNotConnectedError

    async def play(self, gadza_key: str, voice_client: discord.VoiceClient):
        """ Connecting to voice channel and playing Gadza by key. """
        gadza = gadzas_data.get_gadza_by_key(gadza_key)
        print(f"[+] Playing GADZA {gadza.name} - {gadza.duration}")
        voice_client.play(gadza.as_source())


bot.add_cog(GadzaCog(bot))
bot.run(getenv("BOT_TOKEN"), bot=True)

