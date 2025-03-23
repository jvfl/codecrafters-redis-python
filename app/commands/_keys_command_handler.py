import re

from app.io import ConnectionManager
from app.protocol import Resp2Data, Array

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("KEYS")
class KeysCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        pattern = args[0]
        expression = re.compile(pattern.replace("*", ".*"))

        keys = await self._keys_storage.keys()
        results = [key for key in keys if expression.match(key)]

        return Array(results)
