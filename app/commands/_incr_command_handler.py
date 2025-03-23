from app.io import ConnectionManager
from app.storage.key_value.data_types import StringData
from app.protocol import Resp2Data, BulkString, SimpleError, Integer

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("INCR")
class IncrCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        key = args[0]

        value = await self._keys_storage.retrieve(key)

        if value is None:
            return await self._increment_and_store(key, 0)
        elif value and isinstance(value, StringData):
            try:
                int_value = int(value.data)
                return await self._increment_and_store(key, int_value)
            except ValueError:
                return SimpleError("value is not an integer or out of range")
        else:
            return BulkString(None)

    async def _increment_and_store(self, key: str, value: int) -> Resp2Data:
        incremented_value = value + 1
        await self._keys_storage.store(key, StringData(data=f"{incremented_value}"))
        return Integer(incremented_value)
