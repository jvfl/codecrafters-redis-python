from app.storage.key_value import KeyValueStorage
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
from ._wait_command_handler import WaitCommandHandler
from ._type_command_handler import TypeCommandHandler
from ._xadd_command_handler import XAddCommandHandler


class CommandHandlerFactory:
    def __init__(self, keys_storage: KeyValueStorage, config: RedisConfig) -> None:
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
        elif command == "WAIT":
            return WaitCommandHandler(self.config)
        elif command == "TYPE":
            return TypeCommandHandler(self.keys_storage)
        elif command == "XADD":
            return XAddCommandHandler(self.keys_storage)
        else:
            raise NotImplementedError(f"Command {command} is not supported")
