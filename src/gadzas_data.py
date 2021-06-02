from random import choice

import aiohttp

from gadza import Gadza
from gadza_category import GadzaCategory


class GadzasData:
    def __init__(self,
                 gadzas_url: str = "https://raw.githubusercontent.com/VityaSchel/gadzas-online-open-api/main/gadzasData.json"):
        """ Constructor of class
        :param gadzas_url: Url of gadzasData.json. For default is used github file
        """
        self.gadzas_url = gadzas_url
        self.update_gadzas_data()

    @property
    def all(self):
        """ Get all gadzas, without any categories """
        gadzas = []
        for category in self.dict:
            category_object = self.get_category_by_key(category)
            gadzas.append(list(category_object))
        return gadzas

    async def update_gadzas_data(self):
        """ Getting gadzasData from GitHub repozitory and parses it into object variable"""
        async with aiohttp.ClientSession() as session:
            gadzas_data_req = await session.get(self.gadzas_url)
            self.dict: dict = await gadzas_data_req.json()

    def get_gadza_by_key(self, key: str) -> Gadza:
        """ Returns Gadza object by key """
        for category in self.dict.values():
            if key in category:
                return category[key]
        raise KeyError("Gadza doesn't exists!")

    def get_category_by_key(self, key: str) -> GadzaCategory:
        """ Return category of Gadzas """
        category = self.dict[key]
        gadzas = []
        for key, gadza in category.items():
            gadzas.append(Gadza(**gadza, gadza_key=key))
        return GadzaCategory(key, *gadzas)

    def random(self):
        """ Get random Gadza """
        return choice(self.all)
