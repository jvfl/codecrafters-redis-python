import asyncio

from app.io import ConnectionManager
from app.protocol import Resp2Data, Integer, ArrayCodec
from app.server import ReplicaConnection

from ._command_handler import CommandHandler
from ._command_handler_factory import CommandHandlerFactory


@CommandHandlerFactory.register("WAIT")
class WaitCommandHandler(CommandHandler):
    async def handle(self, args: list[str], _: ConnectionManager) -> Resp2Data:
        args[0]  # numreplicas
        timeout = int(args[1]) / 1000.0  # timeout

        ready_replicas: list[ReplicaConnection] = []

        if self._config.master_repl_offset > 0:
            try:
                async with asyncio.timeout(timeout):
                    tasks = []
                    for replica in self._config.replica_connections:
                        task = asyncio.create_task(
                            self._check_replica_readiness(replica, ready_replicas)
                        )
                        tasks.append(task)

                    await asyncio.gather(*tasks)
            except asyncio.TimeoutError:
                print("timeout")
                pass
        else:
            ready_replicas.extend(self._config.replica_connections)

        return Integer(len(ready_replicas))

    async def _check_replica_readiness(
        self, replica: ReplicaConnection, ready_replicas: list[ReplicaConnection]
    ) -> None:
        while True:
            replica_offset = await self._get_replica_offset(
                "REPLCONF GETACK *", replica
            )
            print(
                f"Replica: {replica_offset} Master: {self._config.master_repl_offset}"
            )
            if replica_offset >= self._config.master_repl_offset:
                ready_replicas.append(replica)
                break

    async def _get_replica_offset(
        self, command: str, connection: ReplicaConnection
    ) -> int:
        print("Sending command", command)
        encoded_command = ArrayCodec.encode(command.split(" "))

        await connection.writer.write(encoded_command)

        print("Awaiting response...")
        response = await connection.reader.read(100)
        print("Response", response.decode())
        offset = ArrayCodec.decode(response.decode())[-1]
        return int(offset)
