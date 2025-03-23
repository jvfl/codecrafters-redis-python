from typing import Type, Callable

from app.server import RedisConfig
from app.storage.key_value import KeyValueStorage

from ._command_handler import CommandHandler


class CommandHandlerFactory:
    registry: dict[str, Type[CommandHandler]] = {}

    def __init__(self, keys_storage: KeyValueStorage, config: RedisConfig) -> None:
        self.keys_storage = keys_storage
        self.config = config

    # Based on https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe # noqa
    @classmethod
    def register(cls, key: str) -> Callable[[Type[CommandHandler]], None]:
        def inner_wrapper(command: Type[CommandHandler]) -> None:
            if key in cls.registry:
                raise ValueError(f"CommandHandler for {key} already exists.")
            cls.registry[key] = command

        return inner_wrapper

    def create(self, command_key: str) -> CommandHandler:
        command = CommandHandlerFactory.registry.get(command_key)

        if command is None:
            raise NotImplementedError(f"Command {command_key} is not supported")
        else:
            return command(self.config, self.keys_storage)
