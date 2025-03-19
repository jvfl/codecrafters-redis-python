from app.io import Writer, Reader

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("TYPE")
class TypeCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        key = args[0]

        value = await self._keys_storage.retrieve(key)

        if value:
            await writer.write(value.type())
        else:
            await writer.write("+none\r\n".encode())
