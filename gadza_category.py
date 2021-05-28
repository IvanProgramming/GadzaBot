from gadza import Gadza


class GadzaCategory:
    def __init__(self, key: str, *gadzas: Gadza):
        self.gadzas = gadzas
        self.key = key

    def __iter__(self):
        return self.gadzas

    @property
    def as_dict(self):
        category_dict = {}
        for gadza in self:
            category_dict[gadza.gadza_key] = gadza
