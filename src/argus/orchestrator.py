from argus.resolver.resolver import Resolver
from argus.builder import Builder, Relationship
from argus.connectors.csv_connector import CSVConnector
from argus.mapper import Mapper
from argus.models.entity import Entity
from argus.repositories.sqlite_repository import SQLiteRepository
from argus.resolver.exactmatch_comparer import ExactMatchComparer


class Orchestrator:
    def __init__(self, source_path: str, mapping_path: str, db_path: str):
        self.source_path = source_path
        self.mapping_path = mapping_path
        self.nb_entities = 0
        self.nb_relations = 0

        self.repo = SQLiteRepository(db_path=db_path)

    def run(self) -> None:
        entities = self._csv_to_entities()
        self.nb_entities = sum([len(group) for group in entities])
        self._save_entities(entities)

        builder = Builder(self.mapping_path)
        relations = builder.build(entities)
        self.nb_relations = len(relations)
        self._save_relations(relations)

        resolver = Resolver(self.mapping_path, self.repo, ExactMatchComparer())
        resolver.resolve()

        self.repo.close()

    def _csv_to_entities(self) -> list[list[Entity]]:
        records = CSVConnector().read(self.source_path)
        mapper = Mapper()
        entities = mapper.make_grouped_entities(path=self.mapping_path, records=records)

        return entities

    def _save_entities(self, entities: list[list[Entity]]) -> None:
        self.repo.insert_batch_entities(entities)

    def _save_relations(self, relations: list[Relationship]) -> None:
        self.repo.insert_batch_relations(relations)
