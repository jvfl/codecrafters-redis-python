from app.io import ConnectionManager
from app.protocol import Resp2Data, SimpleString

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("MULTI")
class MultiCommandHandler(CommandHandler):
    async def handle(self, _: list[str], __: ConnectionManager) -> Resp2Data:
        self._config.transaction_mode = []
        return SimpleString.OK()
