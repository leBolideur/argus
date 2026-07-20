from dataclasses import dataclass


@dataclass
class Record:
    source: str
    fields: dict
