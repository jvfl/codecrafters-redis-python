import asyncio

from app.io import Writer, Reader
from app.protocol import ArrayCodec
from app.server import RedisConfig, ReplicaConnection

from ._command_handler import CommandHandler

ARRAY_CODEC = ArrayCodec()


class WaitCommandHandler(CommandHandler):
    def __init__(self, config: RedisConfig):
        self.config = config

    async def handle(self, args: list[str], writer: Writer, _: Reader) -> None:
        args[0]  # numreplicas
        timeout = int(args[1]) / 1000.0  # timeout

        ready_replicas: list[ReplicaConnection] = []

        if self.config.master_repl_offset > 0:
            try:
                async with asyncio.timeout(timeout):
                    tasks = []
                    for replica in self.config.replica_connections:
                        task = asyncio.create_task(
                            self._check_replica_readiness(replica, ready_replicas)
                        )
                        tasks.append(task)

                    await asyncio.gather(*tasks)
            except asyncio.TimeoutError:
                print("timeout")
                pass
        else:
            ready_replicas.extend(self.config.replica_connections)

        response = f":{len(ready_replicas)}\r\n"
        await writer.write(response.encode())

    async def _check_replica_readiness(
        self, replica: ReplicaConnection, ready_replicas: list[ReplicaConnection]
    ) -> None:
        while True:
            replica_offset = await self._get_replica_offset(
                "REPLCONF GETACK *", replica
            )
            print(f"Replica: {replica_offset} Master: {self.config.master_repl_offset}")
            if replica_offset >= self.config.master_repl_offset:
                ready_replicas.append(replica)
                break

    async def _get_replica_offset(
        self, command: str, connection: ReplicaConnection
    ) -> int:
        print("Sending command", command)
        encoded_command = ARRAY_CODEC.encode(command.split(" "))

        await connection.writer.write(encoded_command.encode())

        print("Awaiting response...")
        response = await connection.reader.read(100)
        print("Response", response.decode())
        offset = ARRAY_CODEC.decode(response.decode())[-1]
        return int(offset)
