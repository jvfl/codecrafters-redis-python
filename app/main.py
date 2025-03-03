import asyncio
import typer
import uvloop

from typing import Optional

from app.protocol._array_codec import ArrayCodec
from app.server import RedisServer, RedisConfig, RedisReplicaConfig
from app.storage.keys import InMemoryKeysStorage


APP = typer.Typer()

ARRAY_CODEC = ArrayCodec()


async def run_server(redis_server: RedisServer) -> None:
    print("Server started with the following memory:")
    print(redis_server.keys_storage)

    await redis_server.load_rdb_data()

    replica_info = redis_server.config.replicaof
    if replica_info:
        _, writer = await asyncio.open_connection(replica_info.host, replica_info.port)

        writer.write(ARRAY_CODEC.encode(["PING"]).encode())
        await writer.drain()

    server = await asyncio.start_server(
        redis_server.handle_callback, redis_server.config.host, redis_server.config.port
    )
    async with server:
        await server.serve_forever()


@APP.command()
def main(
    dir: Optional[str] = typer.Option(None),
    dbfilename: Optional[str] = typer.Option(None),
    port: int = typer.Option(6379),
    replicaof: Optional[str] = typer.Option(None),
):
    try:
        print("Starting server with options:")
        print(f"dir: {dir}")
        print(f"dbfilename: {dbfilename}")

        replica_config = None
        if replicaof:
            replicaof_info = replicaof.split(" ")
            replica_config = RedisReplicaConfig(
                replicaof_info[0], int(replicaof_info[1])
            )

        server = RedisServer(
            RedisConfig(
                host="localhost",
                port=port,
                dir=dir,
                dbfilename=dbfilename,
                replicaof=replica_config,
            ),
            InMemoryKeysStorage(),
        )

        uvloop.run(run_server(server))
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error running server: {e}")


if __name__ == "__main__":
    APP()
