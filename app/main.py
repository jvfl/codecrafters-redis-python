import asyncio
from typing import Any

from app.protocol import ArrayCodec, BulkStringCodec
from app.commands import SetCommandHandler

ARRAY_CODEC = ArrayCodec()
STRING_CODEC = BulkStringCodec()

MEMORY: dict[str, Any] = {}

SET_COMMAND_HANDLER = SetCommandHandler(MEMORY)


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

        if command == "PING":
            writer.write(b"+PONG\r\n")
            await writer.drain()
        elif command == "ECHO":
            encoded_string = STRING_CODEC.encode(commandAndArgs[1])
            writer.write(encoded_string.encode("utf-8"))
            await writer.drain()
        elif command == "SET":
            await SET_COMMAND_HANDLER.handle(commandAndArgs, writer)
        elif command == "GET":
            key = commandAndArgs[1]

            if value := MEMORY.get(key):
                encoded_string = STRING_CODEC.encode(value)
                writer.write(encoded_string.encode("utf-8"))
            else:
                writer.write(b"$-1\r\n")
            await writer.drain()

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
