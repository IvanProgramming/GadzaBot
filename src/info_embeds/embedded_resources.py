from json import load
from random import choice


class EmbeddedResources:
    thumbnails_json_path = "res/thumbnails.json"
    quotes_json_path = "res/quotes.json"

    @staticmethod
    def get_thumbnail() -> str:
        thumbnails = load(open(EmbeddedResources.thumbnails_json_path, "r+", encoding="utf-8"))
        return choice(thumbnails)

    @staticmethod
    def get_quote() -> str:
        quotes = load(open(EmbeddedResources.quotes_json_path, "r+", encoding="utf-8"))
        return choice(quotes)
