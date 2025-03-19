from app.io import Writer, Reader

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("PSYNC")
class PsyncCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        args[0]  # master_replid
        args[1]  # master_offset

        response = f"+FULLRESYNC {self._config.master_replid} 0\r\n"
        await writer.write(response.encode())

        with open("resources/empty.rdb", "rb") as state:
            data = state.read()
            fullresync_response = f"${len(data)}\r\n"

        await writer.write(fullresync_response.encode() + data)
