from discord import FFmpegOpusAudio


class Gadza:
    def __init__(self, gadza_key: str, name: str, description: str, duration: int, year: int, source: str,
                 category_key: str, folder_path: str = "./gadzas"):
        """ Constructor of class
        :param category_key: Category key of gadza
        :param name: Gadza name
        :param description: Gadza description
        :param duration: Gadza Duration
        :param year: Gadza Year
        :param source: Gadza source
        :param gadza_key: Gadza key in file gadzaData.json
        """
        self.folder_path = folder_path
        self.source = source
        self.year = year
        self.duration = duration
        self.description = description
        self.name = name
        self.gadza_key = gadza_key
        self.category_key = category_key

    @property
    def file(self):
        """ Return Gadza as File (Don't forget to close!) """
        return open(self.path, 'rb')

    @property
    def path(self):
        return f"{self.folder_path}/{self.category_key}/{self.source}.mp3"

    @property
    def as_dict(self):
        """ Return Gadza as a Dict (As it used in gadzasData.json) """
        return {
            "description": self.description,
            "duration": self.duration,
            "name": self.name,
            "source": self.source,
            "year": self.year
        }

    def as_source(self):
        return FFmpegOpusAudio(self.path)
