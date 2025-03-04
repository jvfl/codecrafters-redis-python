from app.io import Writer
from app.protocol import ArrayCodec
from app.server import RedisConfig

from ._command_handler import CommandHandler

ARRAY_CODEC = ArrayCodec()


class WaitCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = config

    async def handle(self, args: list[str], writer: Writer) -> None:
        _ = args[0]  # numreplicas
        _ = args[1]  # timeout

        ready_replicas = len(self.config.replica_connections)
        response = f":{ready_replicas}\r\n"

        await writer.write(response.encode())
