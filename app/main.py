import socket  # noqa: F401
import asyncio  # noqa: F401


async def handle_callback(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    print("Logs from your program will appear here!")

    while True:
        raw_command = await reader.read(100)
        command = raw_command.decode()

        if command == "":
            break

        pings = [ping for ping in command.splitlines() if ping == "PING"]

        for _ in pings:
            writer.write(b"+PONG\r\n")
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
