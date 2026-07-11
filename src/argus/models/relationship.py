from dataclasses import dataclass


@dataclass
class Relationship:
    id: int
    type: str
    source: int
    target: int
    properties: dict
