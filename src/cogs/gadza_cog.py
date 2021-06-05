import discord
import discord.ext.commands as commands

from src.bot import gadzas_data
from src.exceptions import BaseDiscordException, PermissionConnectError, PermissionSpeakError, UserIsNotConnectedError


class GadzaCog(commands.Cog):
    def __init__(self, bot, gadzas_data):
        self.bot = bot
        self.gadzas_data = gadzas_data

    @commands.command(name="random")
    async def random(self, ctx: commands.Context):
        gadza_key = self.gadzas_data.random().gadza_key
        await self.play(gadza_key, ctx.voice_client)

    @commands.command(name="r")
    async def random_synonym(self, ctx: commands.Context):
        await self.random(ctx)

    @random.before_invoke
    @random_synonym.before_invoke
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
        bot_as_member = await channel.guild.fetch_member(self.bot.user.id)
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
        """ Connecting to voice channel and playing Gadza by key.
        :param gadza_key: Key of Gadza in gadzasData file
        :param voice_client: VoiceClient object for playing audio in it
        """
        gadza = gadzas_data.get_gadza_by_key(gadza_key)
        some_play_instance = voice_client.play(gadza.as_source())
        print(some_play_instance, type(some_play_instance))
