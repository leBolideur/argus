from abc import ABC, abstractmethod

from argus.models.entity import Entity
from argus.models.relationship import Relationship


class BaseRepository(ABC):
    @abstractmethod
    def create_tables(self) -> None:
        pass

    @abstractmethod
    def insert_entity(self, entity: Entity) -> int:
        pass

    @abstractmethod
    def insert_batch_entities(self, batch: list[list[Entity]]) -> list[list[Entity]]:
        pass

    @abstractmethod
    def get_entity(self, id: int) -> Entity | None:
        pass

    @abstractmethod
    def insert_relationship(self, relationship: Relationship) -> int:
        pass

    @abstractmethod
    def insert_batch_relations(
        self, relations: list[Relationship]
    ) -> list[Relationship]:
        pass

    @abstractmethod
    def get_relations_by_source(self, source: int) -> list[Relationship]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
