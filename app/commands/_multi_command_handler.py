from app.io import Writer, Reader

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("MULTI")
class MultiCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        self._config.transaction_mode = []
        await writer.write("+OK\r\n".encode())
