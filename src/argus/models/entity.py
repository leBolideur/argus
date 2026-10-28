from dataclasses import dataclass
from enum import StrEnum


class EntityType(StrEnum):
    UNKNOWN = "UNKNOWN"
    EMAIL = "EMAIL"
    PERSON = "PERSON"


@dataclass
class Entity:
    type: EntityType
    trusted: bool
    source: str
    line: int
    properties: dict
    id: int = 0
