from datetime import datetime
from enum import Enum

from tortoise.fields import DatetimeField, IntField, CharField, ForeignKeyField, JSONField
from tortoise.models import Model

from src.exceptions.administration_exceptions import PrefixTooLong


class Guild(Model):
    id = IntField(pk=True)
    prefix = CharField(max_length=5)

    @staticmethod
    async def add_server(guild_id):
        if await Guild.filter(id=guild_id).count() == 0:
            guild_server = Guild(id=guild_id, prefix="g!")
            await guild_server.save()
        else:
            guild_server = await Guild.filter(id=guild_id).first()
        return guild_server

    @staticmethod
    async def get_prefix(guild_id: int):
        return (await Guild.filter(id=guild_id).first()).prefix

    async def change_prefix(self, new_prefix: str):
        if len(new_prefix) > 5:
            raise PrefixTooLong
        self.prefix = new_prefix
        await self.save()


class PlaybackItem(Model):
    gadza_key = CharField(max_length=32)
    user_id = IntField()
    queue_index = IntField()


class PlaybackState(int, Enum):
    PLAYING = 1
    PAUSED = 2
    NOTHING_PLAYING = 0


class PlaybackQueue(Model):
    guild = ForeignKeyField("models.Guild")
    currently_playing = ForeignKeyField("models.PlaybackItem", null=True)
    last_action = DatetimeField()
    items_json = JSONField(default=[])

    @staticmethod
    async def start_new(guild_id):
        guild = await Guild.filter(id=guild_id).first()
        last_action = datetime.now()
        pq = PlaybackQueue(guild=guild, last_action=last_action, currently_playing=None)
        await pq.save()
        return pq

    async def add_item(self, gadza_key: str, user_id: int):
        in_queue = await PlaybackItem.all().count()
        new_item = PlaybackItem(gadza_key=gadza_key, user_id=user_id, queue_index=in_queue)
        await new_item.save()
        if not self.currently_playing:
            await self.play(new_item)
        self.items_json.append(new_item.id)
        last_action = datetime.now()
        await self.save()
        return new_item

    async def play(self, playback_item: PlaybackItem):
        self.last_action = datetime.now()
        if self.currently_playing:
            await self.skip(self.currently_playing)
        self.currently_playing = playback_item

    async def skip(self, playback_item: PlaybackItem = None):
        if playback_item:
            await self.skip(self.currently_playing)
        self.items_json.remove(playback_item.id)
        self.currently_playing = None
        self.last_action = datetime.now()
        await self.save()
        await playback_item.delete()

    async def play_next(self):
        if self.currently_playing:
            await self.skip()
        if self.items_json:
            next_item = await self.filter(id=self.items_json[0])
            self.currently_playing = next_item
            await self.save()
