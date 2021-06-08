from discord import Embed

from src.gadza import Gadza
from src.info_embeds.embedded_resources import EmbeddedResources


class GadzaInfo:
    def __init__(self, gadza_title: str, description: str, duration: int, year: int, key: str):
        self.title = gadza_title
        self.description = description
        self.duration = duration
        self.year = year
        self.key = key

    @staticmethod
    def from_gadza_object(gadza: Gadza):
        """ Creates GadzaInfo from Gadza object
         :param gadza: Gadz object for generation
         :returns: GadzaInfo object made from Gadza
        """
        return GadzaInfo(gadza.name, gadza.description, gadza.duration, gadza.year, gadza.gadza_key)

    @property
    def site_path(self) -> str:
        """ Path to гадзы.online website """
        return f"https://гадзы.online/#{self.key}"

    @property
    def formatted_time(self) -> str:
        """ Time in format {minutes}:{seconds} """
        seconds = str(self.duration % 60) if self.duration % 60 > 9 else f"0{self.duration % 60}"
        mins = str(self.duration // 60) if self.duration // 60 > 9 else f"0{self.duration // 60}"
        return f"{mins}:{seconds}"

    def to_embed(self) -> Embed:
        """ Returns embed for sending to user """
        output_embed = Embed()
        output_embed.set_thumbnail(url=EmbeddedResources.get_thumbnail())
        output_embed.title = self.title
        if self.description:
            output_embed.add_field(name="Описание гадзы", value=self.description, inline=False)
        output_embed.add_field(name="Год пришествия", value=str(self.year))
        output_embed.add_field(name="Длина гадзы", value=self.formatted_time)
        output_embed.set_footer(text=EmbeddedResources.get_quote())
        return output_embed
