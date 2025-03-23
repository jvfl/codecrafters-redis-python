from app.io import ConnectionManager
from app.protocol import Resp2Data, SimpleString

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("TYPE")
class TypeCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        key = args[0]

        value = await self._keys_storage.retrieve(key)

        if value:
            return SimpleString(value.type())
        else:
            return SimpleString("none")
