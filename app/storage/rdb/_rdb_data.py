from dataclasses import dataclass
from typing import Any

from ._auxiliary_field import AuxiliaryField


@dataclass
class RDBData:
    auxiliary_fields: list[AuxiliaryField]
    hash_table: dict[str, Any]
