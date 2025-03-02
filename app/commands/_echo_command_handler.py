from app.commands._command_handler import CommandHandler
from asyncio import StreamWriter

from app.protocol import BulkStringCodec

STRING_CODEC = BulkStringCodec()


class EchoCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        encoded_string = STRING_CODEC.encode(args[0])
        writer.write(encoded_string.encode("utf-8"))
        await writer.drain()
