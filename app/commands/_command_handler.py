from abc import ABC, abstractmethod

from app.io import Writer, Reader
from app.server import RedisConfig
from app.storage.key_value import KeyValueStorage


class CommandHandler(ABC):
    def __init__(self, config: RedisConfig, keys_storage: KeyValueStorage):
        self._config = config
        self._keys_storage = keys_storage

    @abstractmethod
    async def handle(self, args: list[str], writer: Writer, reader: Reader) -> None:
        raise NotImplementedError
