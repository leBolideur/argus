from dataclasses import dataclass


@dataclass
class Record:
    id: int
    source: str
    fields: dict
