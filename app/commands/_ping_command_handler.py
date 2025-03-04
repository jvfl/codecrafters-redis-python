from app.commands._command_handler import CommandHandler
from app.io import Writer


class PingCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer) -> None:
        await writer.write(b"+PONG\r\n")
