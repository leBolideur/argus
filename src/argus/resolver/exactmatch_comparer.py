from argus.models.entity import Entity
from argus.resolver.base_comparer import BaseComparer


def normalize(input: str | None) -> str | None:
    return None if input is None else input.lower().strip()


class ExactMatchComparer(BaseComparer):
    def __init__(self, property_key: str):
        self.property_key = property_key

    def compare(self, entity1: Entity, entity2: Entity) -> float:
        normal1 = normalize(entity1.properties.get(self.property_key))
        normal2 = normalize(entity2.properties.get(self.property_key))

        return 1.0 if normal1 == normal2 else 0.0
