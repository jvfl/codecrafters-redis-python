from app.io import Writer, Reader
from app.storage.key_value.data_types import StringData

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("INCR")
class IncrCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]

        value = await self._keys_storage.retrieve(key)

        if value and isinstance(value, StringData):
            incremented_value = int(value.data) + 1
            await self._keys_storage.store(key, StringData(data=f"{incremented_value}"))
            await writer.write(f":{incremented_value}\r\n".encode())
        else:
            await writer.write("$-1\r\n".encode())
