from tortoise import Tortoise

from src.settings import DB_URL


async def init_database(safe: bool = True):
    """ Initializes database and generates models
        :param safe: Defines, should tables be overwritten if it already exists
    """
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            "models": ["src.models.models"]
        }
    )
    await Tortoise.generate_schemas(safe=True)
