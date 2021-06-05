import asyncio
from json import loads
from random import choice

import aiohttp
from typing import List

from gadza import Gadza
from gadza_category import GadzaCategory


class GadzasData:
    def __init__(self,
                 gadzas_url: str = "https://raw.githubusercontent.com/VityaSchel/gadzas-online-open-api/main/gadzasData.json"):
        """ Constructor of class
        :param gadzas_url: Url of gadzasData.json. For default is used github file
        """
        self.gadzas_url = gadzas_url

    @property
    def all(self) -> List[Gadza]:
        """ Get all gadzas, without any categories """
        gadzas = []
        for category in self.dict:
            category_object = self.get_category_by_key(category)
            gadzas += list(category_object)
        return gadzas

    async def update_gadzas_data(self):
        """ Getting gadzasData from GitHub repozitory and parses it into object variable"""
        async with aiohttp.ClientSession() as session:
            gadzas_data_req = await session.get(self.gadzas_url)
            gadzas_data_plain = await gadzas_data_req.text()
            self.dict = loads(gadzas_data_plain)

    def get_gadza_by_key(self, key: str) -> Gadza:
        """ Returns Gadza object by key """
        for gadza in self.all:
            if gadza.gadza_key == key:
                return gadza
        raise KeyError("Gadza doesn't exists!")

    def get_category_by_key(self, category_key: str) -> GadzaCategory:
        """ Return category of Gadzas """
        category = self.dict[category_key]
        gadzas = []
        for gadza_key, gadza in category.items():
            gadzas.append(Gadza(gadza_key=gadza_key, category_key=category_key, **gadza))
        return GadzaCategory(gadza_key, *gadzas)

    def random(self) -> Gadza:
        """ Get random Gadza """
        return choice(self.all)
