from app.io import ConnectionManager

from app.storage.key_value.data_types import StringData
from app.protocol import Resp2Data, BulkString, SimpleError

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory

WRONGTYPE_ERROR_MSG = (
    "WRONGTYPE Operation against a key holding the wrong kind of value\r\n"
)


@CommandHandlerFactory.register("GET")
class GetCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        key = args[0]

        value = await self._keys_storage.retrieve(key)

        if value is None:
            return BulkString(None)
        elif isinstance(value, StringData):
            return BulkString(value.data)
        else:
            return SimpleError(WRONGTYPE_ERROR_MSG)
