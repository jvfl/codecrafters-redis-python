from dataclasses import dataclass

from app.io import ConnectionWriter, ConnectionReader


@dataclass
class ReplicaConnection:
    writer: ConnectionWriter
    reader: ConnectionReader
