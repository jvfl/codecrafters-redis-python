import time
import asyncio

from dataclasses import dataclass, field
from pathlib import Path

from ._redis_config import RedisConfig
from app.storage.keys import KeysStorage
from app.storage.rdb import RDBReader, RDBData
from app.commands import CommandHandlerFactory
from app.protocol import ArrayCodec


ARRAY_CODEC = ArrayCodec()


@dataclass
class RedisServer:
    config: RedisConfig
    keys_storage: KeysStorage
    command_factory: CommandHandlerFactory = field(init=False)

    def __post_init__(self):
        self.command_factory = CommandHandlerFactory(self.keys_storage, self.config)

    async def load_rdb_data(self):
        dbfilename_path = Path(f"{self.config.dir}/{self.config.dbfilename}")

        if dbfilename_path.exists():
            data = RDBReader(dbfilename_path).read()
            print("Data read from RDB file:")
            print(data)
        else:
            data = RDBData([], {})
            print("No RDB file found")

        for key, value in data.hash_table.items():
            value, expiry = value

            if expiry is not None:
                expiry_time = expiry - round(time.time() * 1000)
                await self.keys_storage.storeWithExpiration(key, value, expiry_time)
            else:
                await self.keys_storage.store(key, value)

    async def handle_callback(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        print("Logs from your program will appear here!")

        while True:
            raw_command = (await reader.read(100)).decode()
            print("Command:", raw_command)

            if raw_command == "":
                break

            commandAndArgs = ARRAY_CODEC.decode(raw_command)
            command = commandAndArgs[0].upper()
            args = commandAndArgs[1:]

            await self.command_factory.create(command).handle(args, writer)

        writer.close()
        await writer.wait_closed()
