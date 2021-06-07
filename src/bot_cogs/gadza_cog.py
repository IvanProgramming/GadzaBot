import discord
import discord.ext.commands as commands

from src.exceptions import BaseDiscordException, UserIsNotConnectedError, BotIsNotConnectedError, \
    PermissionConnectError, PermissionSpeakError
from src.gadzas_data import GadzasData


class GadzaCog(commands.Cog):
    def __init__(self, bot: discord.Client, gadzas_data: GadzasData):
        """ Playing Gadzas Commands cog constructor """
        self.bot = bot
        self.gadzas_data = gadzas_data

    @commands.command(name="random", aliases=["r", "ран", "рандом"])
    async def random(self, ctx: commands.Context):
        """ Plays random Gadza """
        gadza_key = self.gadzas_data.random().gadza_key
        await self.play(gadza_key, ctx.voice_client)

    @commands.command(name="best", aliases=["b", "лучшие", "бэст"])
    async def best(self, ctx: commands.Context):
        """ Plays random gadza from best category """
        await self.play_random_from_category("best", ctx.voice_client)

    @commands.command(name="classic", aliases=["c", "cls", "класик"])
    async def classic(self, ctx: commands.Context):
        """ Plays random gadza from classic category """
        await self.play_random_from_category("classic", ctx.voice_client)

    @commands.command(name="lite", aliases=["l", "лайт"])
    async def lite(self, ctx: commands.Context):
        """ Plays random gadza from lite category """
        await self.play_random_from_category("lite", ctx.voice_client)

    @commands.command(name="mega", aliases=["m", "мега"])
    async def mega(self, ctx: commands.Context):
        """ Plays random from mega category """
        await self.play_random_from_category("mega", ctx.voice_client)

    @commands.command(name="disconnect", aliases=["leave", "выйти"])
    async def _disconnect(self, ctx: commands.Context):
        """ Disconnects bot from voice channel """
        try:
            await self.disconnect(ctx.voice_client)
        except BaseDiscordException as e:
            await ctx.send(embed=e.to_embed())

    @mega.before_invoke
    @lite.before_invoke
    @classic.before_invoke
    @best.before_invoke
    @random.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        """ Ensure Invoice method, should run before any command, that plays some audio """
        try:
            channel = await self.get_user_channel(ctx.author)
            await self.connect(channel)
        except BaseDiscordException as e:
            await ctx.send(embed=e.to_embed())

    @staticmethod
    async def get_user_channel(member: discord.Member) -> discord.VoiceChannel:
        """ Returns voice channel of user
            :param member: Member object of connected user
            :returns VoiceChannel object. This is VoiceChannel, that user is connected
            :raises UserIsNotConnectedError: user is not connected to any voice channel
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
        gadza = self.gadzas_data.get_gadza_by_key(gadza_key)
        voice_client.play(gadza.as_source())

    async def disconnect(self, voice_client: discord.VoiceClient):
        """ Disconnecting bot from voice channel
            :param voice_client: VoiceClient object
            :raises BotIsNotConnectedError: bot is not connected, so disconnection is not can be performed"""
        if voice_client:
            await voice_client.disconnect()
        else:
            raise BotIsNotConnectedError

    async def connect(self, channel: discord.VoiceChannel):
        """ Connects user to channel, also checking permissions and supress ClientException
        :param channel: Channel to connect
        :raises PermissionConnectError: bot doesn't have permissions for connecting channel
        :raises PermissionSpeakError: bot doesn't have permissions to speak in channel
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

    async def play_random_from_category(self, category_key: str, voice_client: discord.VoiceClient):
        """ Plays random gadza from category and plays it  """
        gadza_key = self.gadzas_data.get_category_by_key(category_key).random().gadza_key
        await self.play(gadza_key, voice_client)
