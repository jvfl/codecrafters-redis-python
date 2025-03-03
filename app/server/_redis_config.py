import random
import string

from dataclasses import dataclass, field
from typing import Optional

from ._redis_replica_config import RedisReplicaConfig


@dataclass
class RedisConfig:
    host: str
    port: int
    dir: Optional[str]
    dbfilename: Optional[str]
    replicaof: Optional[RedisReplicaConfig]
    master_replid: str = field(init=False)
    master_repl_offset: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self.master_replid = "".join(
            random.choices(string.ascii_letters + string.digits, k=40)
        )
