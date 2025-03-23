import random
import string

from dataclasses import dataclass, field
from typing import Optional

from ._replica_connection import ReplicaConnection
from ._redis_node_info import RedisNodeInfo


@dataclass
class RedisConfig:
    host: str
    port: int
    dir: Optional[str]
    dbfilename: Optional[str]
    master_info: Optional[RedisNodeInfo]
    transaction_mode: Optional[list[list[str]]] = field(default=None, init=False)
    master_replid: str = field(init=False)
    master_repl_offset: int = field(default=0, init=False)
    replica_connections: list[ReplicaConnection] = field(
        default_factory=list, init=False
    )
    replica_offset: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self.master_replid = "".join(
            random.choices(string.ascii_letters + string.digits, k=40)
        )
