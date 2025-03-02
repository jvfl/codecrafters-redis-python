from typing import Any
from ._command_handler import CommandHandler
from ._set_command_handler import SetCommandHandler
from ._ping_command_handler import PingCommandHandler
from ._echo_command_handler import EchoCommandHandler
from ._get_command_handler import GetCommandHandler


class CommandHandlerFactory:
    def __init__(self, memory: dict[str, Any]) -> None:
        self.memory = memory

    def create(self, command: str) -> CommandHandler:
        if command == "ECHO":
            return EchoCommandHandler()
        elif command == "GET":
            return GetCommandHandler(self.memory)
        elif command == "SET":
            return SetCommandHandler(self.memory)
        elif command == "PING":
            return PingCommandHandler()
        else:
            raise NotImplementedError(f"Command {command} is not supported")
