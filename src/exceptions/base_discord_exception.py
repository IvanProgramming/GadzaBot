from discord import Embed, Color, User


class BaseDiscordException(Exception):
    """ This is base exception for using in other exceptions """
    is_warning = False
    title = "Something went wrong"
    description = "I don't know what, but something went wrong. Sending report"

    def __init__(self):
        """ For default it doesnt has any parameters, because exception can be used without parameters"""
        pass

    def to_embed(self) -> Embed:
        """ Converting exception to embed to send user """
        result_embed = Embed()
        embed_color = Color.dark_gold() if self.is_warning else Color.dark_red()
        result_embed.description = self.description
        result_embed.title = self.title
        result_embed.colour = embed_color
        return result_embed

    def to_message(self, mention: User = None) -> str:
        """ Converting exception to message, also for sending user
        :param mention: If you want to mention user with this message
        :returns: Message for sending user
        """
        starting_emoji = ":warning:" if self.is_warning else ":octagonal_sign:"
        mention = f" {mention.mention}, " if mention else ""
        return f"{starting_emoji} {mention}*{self.title}*: {self.description}"

    def __str__(self):
        return f"{self.title}: {self.description}"
