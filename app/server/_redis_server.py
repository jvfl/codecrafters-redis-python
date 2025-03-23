import time
import asyncio

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from ._redis_config import RedisConfig
from ._redis_sync_manager import RedisSyncManager
from ._redis_node_info import RedisNodeInfo

from app.storage.key_value import KeyValueStorage
from app.storage.key_value.data_types import StringData
from app.storage.rdb import RDBReader, RDBData
from app.commands import CommandHandlerFactory
from app.protocol import ArrayCodec
from app.io import ConnectionWriter, ConnectionReader, ConnectionManager


@dataclass
class RedisServer:
    config: RedisConfig
    keys_storage: KeyValueStorage
    command_factory: CommandHandlerFactory = field(init=False)
    sync_manager: Optional[RedisSyncManager] = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.command_factory = CommandHandlerFactory(self.keys_storage, self.config)

        master_info = self.config.master_info
        if master_info:
            self.sync_manager = RedisSyncManager(
                current_node_info=RedisNodeInfo(self.config.host, self.config.port),
                master_info=master_info,
                command_factory=self.command_factory,
                config=self.config,
            )

    async def load_rdb_data(self) -> None:
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

        for key, item in data.hash_table.items():
            item, expiry = item
            entry = StringData(item)

            if expiry is not None:
                expiry_time = expiry - round(time.time() * 1000)
                await self.keys_storage.storeWithExpiration(key, entry, expiry_time)
            else:
                await self.keys_storage.store(key, entry)

    async def handle_callback(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        connection_manager = ConnectionManager(
            ConnectionReader(reader), ConnectionWriter(writer)
        )
        while True:
            command_bytes = await reader.read(100)
            raw_command = command_bytes.decode()

            if raw_command == "":
                writer.close()
                await writer.wait_closed()
                break

            commandAndArgs = ArrayCodec.decode(raw_command)
            print("Command:", commandAndArgs)
            command = commandAndArgs[0].upper()
            args = commandAndArgs[1:]

            if self.config.transaction_mode:
                self.config.transaction_mode.append(commandAndArgs)
                writer.write("+QUEUED\r\n".encode())
            else:
                response = await self.command_factory.create(command).handle(
                    args, connection_manager
                )

                if command != "PSYNC":
                    await connection_manager.writer.write(
                        response.resp2_encoded_string().encode()
                    )

                if command == "SET":
                    for conn in self.config.replica_connections:
                        await conn.writer.write(command_bytes)
                    self.config.master_repl_offset += len(
                        ArrayCodec.encode(commandAndArgs)
                    )
                elif command == "PSYNC":
                    break

    async def sync_with_master(self) -> None:
        if self.sync_manager:
            await self.sync_manager.sync_with_master()
