import asyncio
from typing import Any


class SetCommandHandler:
    def __init__(self, memory: dict[Any, Any]):
        self.memory = memory

    async def handle(
        self, commandAndArgs: list[str], writer: asyncio.StreamWriter
    ) -> None:
        key = commandAndArgs[1]
        value = commandAndArgs[2]

        self.memory[key] = value

        # Handle expiration if PX option is present
        if len(commandAndArgs) > 3 and commandAndArgs[3].lower() == "px":
            try:
                px_value = int(commandAndArgs[4])
                asyncio.create_task(self._expire_key(key, px_value))
            except (ValueError, IndexError):
                writer.write(b"-ERR Invalid PX value\r\n")
                await writer.drain()

        writer.write(b"+OK\r\n")
        await writer.drain()

    async def _expire_key(self, key: str, delay_ms: int) -> None:
        await asyncio.sleep(delay_ms / 1000.0)  # Convert ms to seconds
        self.memory.pop(key, None)
