import csv

from argus.connectors.base_connector import BaseConnector
from argus.models.record import Record


class CSVConnector(BaseConnector):
    def read(self, path: str) -> list[Record]:
        with open(path, encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [
                Record(source=path, line=line, fields=row)
                for (line, row) in enumerate(reader)
            ]
