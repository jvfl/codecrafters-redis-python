from abc import ABC, abstractmethod

from app.io import ConnectionManager
from app.server import RedisConfig
from app.storage.key_value import KeyValueStorage
from app.protocol import Resp2Data


class CommandHandler(ABC):
    def __init__(self, config: RedisConfig, keys_storage: KeyValueStorage):
        self._config = config
        self._keys_storage = keys_storage

    @abstractmethod
    async def handle(self, args: list[str], connection: ConnectionManager) -> Resp2Data:
        raise NotImplementedError
