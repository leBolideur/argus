from abc import ABC, abstractmethod

from argus.models.entity import Entity


class BaseComparer(ABC):
    @abstractmethod
    def compare(self, entity1: Entity, entity2: Entity, property_key: str) -> float:
        pass
