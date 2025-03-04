from app.commands._command_handler import CommandHandler
from app.io import Writer, Reader


class PingCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        await writer.write(b"+PONG\r\n")
