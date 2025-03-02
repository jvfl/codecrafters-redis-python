from app.commands._command_handler import CommandHandler
from asyncio import StreamWriter


class PingCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        writer.write(b"+PONG\r\n")
        await writer.drain()
