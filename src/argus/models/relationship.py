from dataclasses import dataclass


@dataclass
class Relationship:
    type: str
    source: int
    target: int
    properties: dict
    id: int = 0
