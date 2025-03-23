from app.io import ConnectionManager
from app.protocol import Resp2Data, SimpleString

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("PING")
class PingCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        return SimpleString("PONG")
