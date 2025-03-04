from asyncio import StreamWriter

from app.protocol import BulkStringCodec
from app.server import RedisConfig

from ._command_handler import CommandHandler

STRING_CODEC = BulkStringCodec()


class PsyncCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = config

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        master_replid = args[0]
        master_offset = args[1]

        response = f"+FULLRESYNC {self.config.master_replid} 0\r\n"
        writer.write(response.encode())
        await writer.drain()

        with open("resources/empty.rdb", "rb") as state:
            data = state.read()
            fullresync_response = f"${len(data)}\r\n"

            writer.write(fullresync_response.encode() + data)
            await writer.drain()
