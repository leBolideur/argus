from argus.builder import Builder, Relationship
from argus.connectors.csv_connector import CSVConnector
from argus.mapper import Mapper
from argus.models.entity import Entity
from argus.repositories.sqlite_repository import SQLiteRepository


class Orchestrator:
    def __init__(self, source_path: str, mapping_path: str, db_path: str):
        self.source_path = source_path
        self.mapping_path = mapping_path

        self.repository = SQLiteRepository(db_path=db_path)

    def run(self) -> None:
        entities = self.csv_to_entities()
        self.save_entities(entities)
        builder = Builder(self.mapping_path)
        relations = builder.build(entities)
        self.save_relations(relations)

    def csv_to_entities(self) -> list[list[Entity]]:
        records = CSVConnector().read(self.source_path)
        mapper = Mapper()
        entities = mapper.make_grouped_entities(path=self.mapping_path, records=records)

        return entities

    def save_entities(self, entities: list[list[Entity]]) -> None:
        self.entities = self.repository.insert_batch_entities(entities)

    def save_relations(self, relations: list[Relationship]) -> None:
        self.relations = self.repository.insert_batch_relations(relations)
