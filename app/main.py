import asyncio
import typer
import uvloop
import traceback

from typing import Optional


from app.server import RedisServer, RedisConfig, RedisNodeInfo
from app.storage.key_value import InMemoryStorage


APP = typer.Typer()


async def run_server(redis_server: RedisServer) -> None:
    await redis_server.load_rdb_data()

    print("Server started with the following memory:")
    print(redis_server.keys_storage)
    print()

    server = await asyncio.start_server(
        redis_server.handle_callback, redis_server.config.host, redis_server.config.port
    )
    async with server:
        await redis_server.sync_with_master()
        await server.serve_forever()


@APP.command()
def main(
    dir: Optional[str] = typer.Option(None),
    dbfilename: Optional[str] = typer.Option(None),
    port: int = typer.Option(6379),
    replicaof: Optional[str] = typer.Option(None),
) -> None:
    try:
        replica_config = None
        if replicaof:
            replicaof_info = replicaof.split(" ")
            replica_config = RedisNodeInfo(replicaof_info[0], int(replicaof_info[1]))

        config = RedisConfig(
            host="localhost",
            port=port,
            dir=dir,
            dbfilename=dbfilename,
            master_info=replica_config,
        )

        print("Starting server with config:")
        print(config)
        print()

        server = RedisServer(config, InMemoryStorage())

        uvloop.run(run_server(server))
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error running server: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    APP()
