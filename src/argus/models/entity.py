from dataclasses import dataclass


@dataclass
class Entity:
    type: str
    properties: dict
    id: int = 0
