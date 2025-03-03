from dataclasses import dataclass
from typing import Optional


@dataclass
class RedisConfig:
    host: str
    port: int
    dir: Optional[str]
    dbfilename: Optional[str]
