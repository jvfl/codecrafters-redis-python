from app.storage.keys import KeysStorage
from app.server import RedisConfig

from ._command_handler import CommandHandler
from ._set_command_handler import SetCommandHandler
from ._ping_command_handler import PingCommandHandler
from ._echo_command_handler import EchoCommandHandler
from ._get_command_handler import GetCommandHandler
from ._config_command_handler import ConfigCommandHandler
from ._keys_command_handler import KeysCommandHandler
from ._info_command_handler import InfoCommandHandler
from ._replconf_command_handler import ReplConfCommandHandler
from ._psync_command_handler import PsyncCommandHandler


class CommandHandlerFactory:
    def __init__(self, keys_storage: KeysStorage, config: RedisConfig) -> None:
        self.keys_storage = keys_storage
        self.config = config

    def create(self, command: str) -> CommandHandler:
        if command == "ECHO":
            return EchoCommandHandler()
        elif command == "GET":
            return GetCommandHandler(self.keys_storage)
        elif command == "SET":
            return SetCommandHandler(self.keys_storage)
        elif command == "PING":
            return PingCommandHandler()
        elif command == "CONFIG":
            return ConfigCommandHandler(self.config)
        elif command == "KEYS":
            return KeysCommandHandler(self.keys_storage)
        elif command == "INFO":
            return InfoCommandHandler(self.config)
        elif command == "REPLCONF":
            return ReplConfCommandHandler(self.config)
        elif command == "PSYNC":
            return PsyncCommandHandler(self.config)
        else:
            raise NotImplementedError(f"Command {command} is not supported")
