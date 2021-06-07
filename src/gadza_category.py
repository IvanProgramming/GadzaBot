from gadza import Gadza
from random import choice


class GadzaCategory:
    """ This is class for Category of Gadza """

    def __init__(self, key: str, *gadzas: Gadza):
        """ Constructor of class
        :param key: Key of category in gadzasData.json
        :param gadzas: List of gadzas, listed in category
        """
        self.gadzas = gadzas
        self.key = key

    def __iter__(self):
        return self.gadzas.__iter__()

    @property
    def as_dict(self):
        """ Returns category as it presented in gadzasData.json """
        category_dict = {}
        for gadza in self:
            category_dict[gadza.gadza_key] = gadza
        return category_dict

    def random(self) -> Gadza:
        """ Returns random gadza from category """
        return choice(self)
