from dataclasses import dataclass


@dataclass
class RedisReplicaConfig:
    host: str
    port: int
