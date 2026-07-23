import tomllib

from argus.models.relationship import Relationship
from argus.models.entity import Entity


class Builder:
    def __init__(self, mapping_path: str) -> None:
        self.relations_map = []

        with open(mapping_path, "rb") as file:
            mapping = tomllib.load(file)
            for relationship in mapping["relationships"]:
                self.relations_map.append(relationship)

    def build(self, grouped_entities: list[list[Entity]]) -> list[Relationship]:
        relations: list[Relationship] = []
        for entities in grouped_entities:
            for relation in self.relations_map:
                source = self._find_entity_by_source(relation["source"], entities)
                target = self._find_entity_by_source(relation["target"], entities)
                if source is not None and target is not None:
                    relation = Relationship(relation["type"], source.id, target.id, {})
                    relations.append(relation)

        return relations

    def _find_entity_by_source(
        self, source: str, grouped_entities: list[Entity]
    ) -> Entity | None:
        return list(filter(lambda entity: entity.type == source, grouped_entities))[0]

    def _find_entity_by_target(
        self, target: str, grouped_entities: list[Entity]
    ) -> Entity | None:
        return list(filter(lambda entity: entity.type == target, grouped_entities))[0]
