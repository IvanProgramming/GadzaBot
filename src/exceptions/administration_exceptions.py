from src.exceptions import BaseDiscordException


class AdministrationPermsRequired(BaseDiscordException):
    title = "Низя!"
    description = "Я не могу этого сделать, попроси модератора, у него должно получиться"


class PrefixTooLong(BaseDiscordException):
    title = "Слишком длинный префикс"
    description = "Префикс слишком длинный, максимальная длина префикса - 5 символов"
