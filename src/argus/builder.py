from argus.models.relationship import Relationship
from argus.models.entity import Entity


class Builder:
    def __init__(self) -> None:
        pass

    def build(self, grouped_entities: list[list[Entity]]) -> list[Relationship]:
        relations: list[Relationship] = []
        # for entities in grouped_entities:
        #     for relation in self.relations_map:
        #         source = self._find_entity_by_type(relation["source"], entities)
        #         target = self._find_entity_by_type(relation["target"], entities)
        #         if source is not None and target is not None:
        #             relation = Relationship(relation["type"], source.id, target.id, {})
        #             relations.append(relation)

        return relations

    def _find_entity_by_type(
        self, type: str, grouped_entities: list[Entity]
    ) -> Entity | None:
        entities = list(filter(lambda entity: entity.type == type, grouped_entities))
        if len(entities) > 0:
            return entities[0]

        return None
