import time
import asyncio

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ._redis_config import RedisConfig
from ._redis_sync_manager import RedisSyncManager
from ._redis_node_info import RedisNodeInfo

from app.storage.keys import KeysStorage
from app.storage.rdb import RDBReader, RDBData
from app.commands import CommandHandlerFactory
from app.protocol import ArrayCodec
from app.io import ConnectionWriter, ConnectionReader

ARRAY_CODEC = ArrayCodec()


@dataclass
class RedisServer:
    config: RedisConfig
    keys_storage: KeysStorage
    command_factory: CommandHandlerFactory = field(init=False)
    sync_manager: Optional[RedisSyncManager] = field(init=False, default=None)

    def __post_init__(self):
        self.command_factory = CommandHandlerFactory(self.keys_storage, self.config)

        master_info = self.config.master_info
        if master_info:
            self.sync_manager = RedisSyncManager(
                current_node_info=RedisNodeInfo(self.config.host, self.config.port),
                master_info=master_info,
                command_factory=self.command_factory,
                config=self.config,
            )

    async def load_rdb_data(self):
        dbfilename_path = Path(f"{self.config.dir}/{self.config.dbfilename}")

        if dbfilename_path.exists():
            data = RDBReader(dbfilename_path).read()
            print("Data read from RDB file:")
            print(data)
            print()
        else:
            data = RDBData([], {})
            print("No RDB file found")
            print()

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
        while True:
            command_bytes = await reader.read(100)
            raw_command = command_bytes.decode()
            print("Command:", raw_command)

            if raw_command == "":
                writer.close()
                await writer.wait_closed()
                break

            commandAndArgs = ARRAY_CODEC.decode(raw_command)
            command = commandAndArgs[0].upper()
            args = commandAndArgs[1:]

            await self.command_factory.create(command).handle(
                args, ConnectionWriter(writer), ConnectionReader(reader)
            )

            if command == "SET":
                for conn in self.config.replica_connections:
                    await conn.writer.write(command_bytes)
                self.config.master_repl_offset += len(
                    ARRAY_CODEC.encode(commandAndArgs).encode()
                )
            elif command == "PSYNC":
                break

    async def sync_with_master(self):
        if self.sync_manager:
            await self.sync_manager.sync_with_master()
