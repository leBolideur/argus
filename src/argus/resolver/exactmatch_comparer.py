from argus.models.entity import Entity
from argus.resolver.base_comparer import BaseComparer


def _normalize(input: str | None) -> str | None:
    return None if input is None else input.lower().strip()


class ExactMatchComparer(BaseComparer):
    def compare(self, entity1: Entity, entity2: Entity, property_key: str) -> float:
        normal1 = _normalize(entity1.properties.get(property_key))
        normal2 = _normalize(entity2.properties.get(property_key))

        return 1.0 if normal1 == normal2 else 0.0
