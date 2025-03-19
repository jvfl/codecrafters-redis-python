from app.io import Writer, Reader

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("GET")
class GetCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]

        value = await self._keys_storage.retrieve(key)

        if value:
            await writer.write(value.encode())
        else:
            await writer.write("$-1\r\n".encode())
