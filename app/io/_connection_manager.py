import uuid

from dataclasses import dataclass, field

from ._writer import Writer
from ._reader import Reader


@dataclass
class ConnectionManager:
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    reader: Reader
    writer: Writer
