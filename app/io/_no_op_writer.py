from ._writer import Writer


class NoOpWriter(Writer):
    async def write(self, _: bytes) -> None:
        pass
