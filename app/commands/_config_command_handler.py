from dataclasses import asdict
from typing import Any

from app.io import ConnectionManager
from app.protocol import Resp2Data, Array

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("CONFIG")
class ConfigCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        subcommand = args[0]

        if subcommand == "GET":
            return Array(await self.handle_get(args[1:]))

        return Array([])

    async def handle_get(self, args: list[str]) -> list[Any]:
        config_key = args[0]

        return [config_key, asdict(self._config)[config_key]]
