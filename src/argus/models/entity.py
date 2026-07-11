from dataclasses import dataclass


@dataclass
class Entity:
    id: int
    type: str
    properties: dict
