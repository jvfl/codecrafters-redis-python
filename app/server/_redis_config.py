from dataclasses import dataclass
from typing import Optional

from ._redis_replica_config import RedisReplicaConfig


@dataclass
class RedisConfig:
    host: str
    port: int
    dir: Optional[str]
    dbfilename: Optional[str]
    replicaof: Optional[RedisReplicaConfig]
