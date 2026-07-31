import tomllib

from argus.resolver.merger import Merger
from argus.repositories.base_repository import BaseRepository
from argus.resolver.base_comparer import BaseComparer


class Resolver:
    def __init__(self, mapping_path: str, repo: BaseRepository, comparer: BaseComparer):
        self.mapping_path = mapping_path
        self.repo = repo
        self.comparer = comparer

    def resolve(self):
        unique_keys = self._get_unique_keys()
        if len(unique_keys) == 0:
            return

        # TODO: Handle multiple keys
        key = unique_keys[0]

        entity_type, _, prop_key = key
        entities = self.repo.get_all_entities_by_type(entity_type)

        merger = Merger(self.repo)
        for i, e1 in enumerate(entities):
            rest = entities[i + 1 :]
            for e2 in rest:
                if (not e1.properties[prop_key]) or (not e2.properties[prop_key]):
                    continue

                if self.comparer.compare(e1, e2, property_key=prop_key) == 1.0:
                    print(f"\ne1: {e1}")
                    print(f"e2: {e2}\n")
                    merger.merge(e1, e2)

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
