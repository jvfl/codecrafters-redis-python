import asyncio
import typer
import uvloop
import time

from typing import Any, Optional
from pathlib import Path

from app.protocol import ArrayCodec
from app.commands import CommandHandlerFactory
from app.storage.rdb import RDBReader, RDBData


APP = typer.Typer()

ARRAY_CODEC = ArrayCodec()

MEMORY: dict[str, Any] = {}
CONFIG_MEMORY: dict[str, Any] = {}

COMMAND_HANDLER_FACTORY = CommandHandlerFactory(MEMORY, CONFIG_MEMORY)


async def handle_callback(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    print("Logs from your program will appear here!")

    while True:
        raw_command = (await reader.read(100)).decode()
        print("Command:", raw_command)

        if raw_command == "":
            break

        commandAndArgs = ARRAY_CODEC.decode(raw_command)
        command = commandAndArgs[0]
        args = commandAndArgs[1:]

        await COMMAND_HANDLER_FACTORY.create(command).handle(args, writer)

    writer.close()
    await writer.wait_closed()


async def run_server(host: str, port: int, data: RDBData) -> None:
    for key, value in data.hash_table.items():
        value, expiry = value
        MEMORY[key] = value
        if expiry is not None:
            expiry_time = expiry - round(time.time() * 1000)

            print(key, expiry, expiry_time)
            asyncio.create_task(_expire_key(key, expiry_time))

    print("Server started with the following memory:")
    print(MEMORY)

    server = await asyncio.start_server(handle_callback, host, port)
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

        if dir is not None:
            CONFIG_MEMORY["dir"] = dir
        if dbfilename is not None:
            CONFIG_MEMORY["dbfilename"] = dbfilename

        dbfilename_path = Path(
            f"{CONFIG_MEMORY.get('dir')}/{CONFIG_MEMORY.get('dbfilename')}"
        )
        if dbfilename_path.exists():
            data = RDBReader(dbfilename_path).read()
            print("Data read from RDB file:")
            print(data)
        else:
            data = RDBData([], {})
            print("No RDB file found")

        uvloop.run(run_server("localhost", port, data))
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error running server: {e}")


async def _expire_key(key: str, delay_ms: int) -> None:
    await asyncio.sleep(delay_ms / 1000.0)  # Convert ms to seconds
    MEMORY.pop(key, None)


if __name__ == "__main__":
    APP()
