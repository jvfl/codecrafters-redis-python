from app.commands._command_handler import CommandHandler
from app.io import Writer, Reader

from app.protocol import BulkStringCodec

STRING_CODEC = BulkStringCodec()


class EchoCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        encoded_string = STRING_CODEC.encode(args[0])
        await writer.write(encoded_string.encode())
