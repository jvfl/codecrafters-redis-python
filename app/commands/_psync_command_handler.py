from app.io import Writer, Reader
from app.protocol import BulkStringCodec
from app.server import RedisConfig

from ._command_handler import CommandHandler

STRING_CODEC = BulkStringCodec()


class PsyncCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = config

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        args[0]  # master_replid
        args[1]  # master_offset

        response = f"+FULLRESYNC {self.config.master_replid} 0\r\n"
        await writer.write(response.encode())

        with open("resources/empty.rdb", "rb") as state:
            data = state.read()
            fullresync_response = f"${len(data)}\r\n"

        await writer.write(fullresync_response.encode() + data)
