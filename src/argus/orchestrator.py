from argus.connectors.csv_connector import CSVConnector
from argus.models.entity import Entity
from argus.repositories.sqlite_repository import SQLiteRepository
from argus.validator import Validator


class Orchestrator:
    def __init__(self, source_path: str, db_path: str):
        self.source_path = source_path
        self.nb_entities = 0
        self.nb_relations = 0

        self.repo = SQLiteRepository(db_path=db_path)

    def run(self) -> list | None:
        entities = self._csv_to_entities()
        self.nb_entities = sum([len(group) for group in entities])
        self._save_entities(entities)

        self.repo.close()

        return []

    def _csv_to_entities(self) -> list[list[Entity]]:
        records = CSVConnector().read(self.source_path)
        validator = Validator()
        entities = validator.make_grouped_entities(records=records)

        return entities

    def _save_entities(self, entities: list[list[Entity]]) -> None:
        self.repo.insert_batch_entities(entities)
