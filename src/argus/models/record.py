from dataclasses import dataclass


@dataclass
class Record:
    source: str
    line: int
    fields: dict
