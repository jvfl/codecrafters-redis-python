from dataclasses import dataclass


@dataclass
class RedisNodeInfo:
    host: str
    port: int
