from typing import Any
from ._command_handler import CommandHandler
from ._set_command_handler import SetCommandHandler
from ._ping_command_handler import PingCommandHandler
from ._echo_command_handler import EchoCommandHandler
from ._get_command_handler import GetCommandHandler
from ._config_command_handler import ConfigCommandHandler
from ._keys_command_handler import KeysCommandHandler


class CommandHandlerFactory:
    def __init__(self, memory: dict[str, Any], config_memory: dict[str, Any]) -> None:
        self.memory = memory
        self.config_memory = config_memory

    def create(self, command: str) -> CommandHandler:
        if command == "ECHO":
            return EchoCommandHandler()
        elif command == "GET":
            return GetCommandHandler(self.memory)
        elif command == "SET":
            return SetCommandHandler(self.memory)
        elif command == "PING":
            return PingCommandHandler()
        elif command == "CONFIG":
            return ConfigCommandHandler(self.config_memory)
        elif command == "KEYS":
            return KeysCommandHandler(self.memory)
        else:
            raise NotImplementedError(f"Command {command} is not supported")
