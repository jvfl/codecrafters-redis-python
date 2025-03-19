import re

from app.io import Writer, Reader
from app.protocol import ArrayCodec

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("KEYS")
class KeysCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        pattern = args[0]
        expression = re.compile(pattern.replace("*", ".*"))

        keys = await self._keys_storage.keys()
        results = [key for key in keys if expression.match(key)]

        await writer.write(ArrayCodec.encode(results))
