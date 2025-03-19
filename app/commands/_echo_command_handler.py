from app.io import Writer, Reader
from app.protocol import BulkStringCodec

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("ECHO")
class EchoCommandHandler(CommandHandler):
    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        encoded_string = BulkStringCodec.encode(args[0])
        await writer.write(encoded_string)
