import asyncio
from asyncio import StreamWriter
from typing import Any
from ._command_handler import CommandHandler


class SetCommandHandler(CommandHandler):
    def __init__(self, memory: dict[Any, Any]):
        self.memory = memory

    async def handle(self, args: list[str], writer: StreamWriter) -> None:
        key = args[0]
        value = args[1]

        self.memory[key] = value

        # Handle expiration if PX option is present
        if len(args) > 3 and args[2].lower() == "px":
            try:
                px_value = int(args[3])
                asyncio.create_task(self._expire_key(key, px_value))
            except (ValueError, IndexError):
                writer.write(b"-ERR Invalid PX value\r\n")
                await writer.drain()

        writer.write(b"+OK\r\n")
        await writer.drain()

    async def _expire_key(self, key: str, delay_ms: int) -> None:
        await asyncio.sleep(delay_ms / 1000.0)  # Convert ms to seconds
        self.memory.pop(key, None)
