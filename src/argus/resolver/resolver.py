import tomllib
from dataclasses import dataclass

from argus.models.entity import Entity
from argus.resolver.exactmatch_comparer import ExactMatchComparer


@dataclass
class Doublon:
    entity_type: str
    prop_key: str
    normalized_value: str
    entities: list[Entity]


class Resolver:
    def __init__(self, mapping_path: str):
        self.mapping_path = mapping_path
        self.comparer = ExactMatchComparer()

    def resolve(self, grouped_entities: list[list[Entity]]):
        unique_keys = self._get_unique_keys()
        if len(unique_keys) == 0:
            return

        # TODO: Handle multiple keys
        key = unique_keys[0]

        entity_type, _, prop_key = key

        doublons = self._search_doublons(entity_type, prop_key, grouped_entities)

        return doublons

    def _search_doublons(
        self, entity_type: str, prop_key: str, grouped_entities: list[list[Entity]]
    ) -> list[Doublon]:
        doublons: dict[str, list[Entity]] = {}
        for group in grouped_entities:
            for entity in group:
                if entity.type != entity_type:
                    continue

                discriminent = self.comparer.get_key(entity, prop_key)
                if discriminent in doublons.keys():
                    doublons[discriminent].append(entity)
                else:
                    doublons[discriminent] = [entity]

        doublons = {key: value for key, value in doublons.items() if len(value) > 1}

        result = []
        for key, val in doublons.items():
            d = Doublon(entity_type, prop_key, normalized_value=key, entities=val)
            result.append(d)

        return result

    def _get_unique_keys(self) -> list[list[str]]:
        keys = []
        with open(self.mapping_path, "rb") as map:
            mapping = tomllib.load(map)
            for key in mapping["columns"]:
                if mapping["columns"][key].get("unique") is True:
                    entity = mapping["columns"][key]["entity"]
                    property = mapping["columns"][key]["property"]
                    keys.append([entity, key, property])

        return keys
