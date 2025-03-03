from dataclasses import dataclass
from typing import Union


@dataclass
class AuxiliaryField:
    name: str
    value: Union[str | int]
