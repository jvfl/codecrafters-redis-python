import asyncio
import typer
import uvloop

from typing import Optional


from app.server import RedisServer, RedisConfig, RedisNodeInfo, RedisSyncManager
from app.storage.keys import InMemoryKeysStorage


APP = typer.Typer()


async def run_server(redis_server: RedisServer) -> None:
    print("Server started with the following memory:")
    print(redis_server.keys_storage)

    await redis_server.load_rdb_data()

    server = await asyncio.start_server(
        redis_server.handle_callback, redis_server.config.host, redis_server.config.port
    )
    async with server:
        master_info = redis_server.config.master_info
        if master_info:
            sync_manager = RedisSyncManager(
                current_node_info=RedisNodeInfo(
                    redis_server.config.host, redis_server.config.port
                ),
                master_info=master_info,
            )
            await sync_manager.sync_with_master()

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
            replica_config = RedisNodeInfo(replicaof_info[0], int(replicaof_info[1]))

        server = RedisServer(
            RedisConfig(
                host="localhost",
                port=port,
                dir=dir,
                dbfilename=dbfilename,
                master_info=replica_config,
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
