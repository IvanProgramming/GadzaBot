from src.exceptions.base_discord_exception import BaseDiscordException


class PermissionConnectError(BaseDiscordException):
    """ Bot can't connect to voice channel """
    title = "Прав нема!"
    description = "Не могу подключится, выдайте права!"


class PermissionSpeakError(BaseDiscordException):
    """ Bot can't speak in voice channel """
    title = "I CANT SPEAK"
    description = "Дайте право говорить в канале"
    is_warning = True


class UserIsNotConnectedError(BaseDiscordException):
    """ Member, that requested error doesn't connected to voice channel """
    title = "Сначала зайди"
    description = "Зайдите в голосовой канал, прежде чем пользоваться ботом!"


class BotIsMutedError(BaseDiscordException):
    """ Bot can't speak, because it is muted """
    title = "Включите мне микрофон"
    description = "Мне замьютили микрофон на сервере, размьютьте пожалуйста"


class BotIsNotConnectedError(BaseDiscordException):
    """ Bot can't disconnect from channel, because he is not connected """
    title = "Каво?"
    description = "Вы мне, уважаемому боту, предлагаете отключиться от ничего?"
    is_warning = True


class PlaybackIsNotPausedError(BaseDiscordException):
    title = "Зачем?"
    description = "Как можно продолжить воспроизведение того, что на паузе не стоит?"
    is_warning = True
