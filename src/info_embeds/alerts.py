from discord import Embed, Color


class BaseAlert:
    color_hex = "#000000"
    colour_object = None

    def __init__(self, title, description):
        self.title = title
        self.description = description

    @staticmethod
    def hex2rgb(hex_str: str):
        if len(hex_str) == 7:
            r = int(hex_str[1:3], base=16)
            g = int(hex_str[3:5], base=16)
            b = int(hex_str[5:7], base=16)
        elif len(hex_str) == 4:
            r = int(hex_str[1:2], base=16)
            g = int(hex_str[2:3], base=16)
            b = int(hex_str[3:4], base=16)
        elif len(hex_str) == 3:
            r, g, b = [int(hex_str[1:], base=16)] * 3
        else:
            raise ValueError("Incorrect color code")
        return r, g, b

    def as_embed(self):
        embed = Embed()
        embed.title = self.title
        embed.description = self.description
        embed.colour = Color.from_rgb(*self.hex2rgb(self.color_hex))
        if self.colour_object:
            embed.colour = self.colour_object
        return embed


class SuccessAlert(BaseAlert):
    colour_object = Color.green()


class InfoAlert(BaseAlert):
    colour_object = Color.blue()


class PrefixSetSuccessful(SuccessAlert):
    def __init__(self, new_prefix):
        description = f"Префикс успешно изменен на `{new_prefix}`"
        title = "Успешно изменено"
        super().__init__(title, description)
