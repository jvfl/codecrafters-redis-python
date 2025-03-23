from app.io import ConnectionManager
from app.protocol import Resp2Data, SimpleError, Array

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("EXEC")
class ExecCommandHandler(CommandHandler):
    async def handle(self, _: list[str], __: ConnectionManager) -> Resp2Data:
        if self._config.transaction_mode is None:
            return SimpleError("EXEC without MULTI")

        return Array([])
