import asyncio
from typing import Any

from app.protocol import ArrayCodec
from app.commands import CommandHandlerFactory

ARRAY_CODEC = ArrayCodec()

MEMORY: dict[str, Any] = {}

COMMAND_HANDLER_FACTORY = CommandHandlerFactory(MEMORY)


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


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(handle_callback, host, port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(run_server("localhost", 6379))
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error running server: {e}")
