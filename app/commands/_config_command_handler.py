from app.io import Writer
from dataclasses import asdict

from app.server import RedisConfig
from app.protocol import ArrayCodec

from ._command_handler import CommandHandler

ARRAY_CODEC = ArrayCodec()


class ConfigCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = asdict(config)

    async def handle(self, args: list[str], writer: Writer) -> None:
        subcommand = args[0]

        if subcommand == "GET":
            await self.handle_get(args[1:], writer)

    async def handle_get(self, args: list[str], writer: Writer) -> None:
        config_key = args[0]

        response = ARRAY_CODEC.encode([config_key, self.config[config_key]])
        await writer.write(response.encode())
