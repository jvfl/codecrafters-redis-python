import asyncio
import typer
import uvloop

from typing import Optional

from app.server import RedisServer, RedisConfig
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
        await server.serve_forever()


@APP.command()
def main(
    dir: Optional[str] = typer.Option(None),
    dbfilename: Optional[str] = typer.Option(None),
    port: int = typer.Option(6379),
):
    try:
        print("Starting server with options:")
        print(f"dir: {dir}")
        print(f"dbfilename: {dbfilename}")

        server = RedisServer(
            RedisConfig("localhost", port, dir, dbfilename), InMemoryKeysStorage()
        )

        uvloop.run(run_server(server))
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error running server: {e}")


if __name__ == "__main__":
    APP()
