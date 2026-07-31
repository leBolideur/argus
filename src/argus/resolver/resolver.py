import tomllib

from argus.repositories.base_repository import BaseRepository


class Resolver:
    def __init__(self, mapping_path: str, repo: BaseRepository):
        self.mapping_path = mapping_path
        self.repo = repo

    def resolve(self):
        unique_keys = self._get_unique_keys()
        # TODO: Handle multiple keys
        key = unique_keys[0]
        print(key)

        entity, k = key
        entities = self.repo.get_all_entities_by_type(entity)
        doublon = 0
        values = set()
        for entity in entities:
            property = entity.properties.get(k)
            values.add(property)
            if property in values:
                doublon += 1

        print(doublon)
        print(values)

    def _get_unique_keys(self) -> list[list[str]]:
        keys = []
        with open(self.mapping_path, "rb") as map:
            mapping = tomllib.load(map)
            for key in mapping["columns"]:
                if mapping["columns"][key].get("unique") is True:
                    entity = mapping["columns"][key]["entity"]
                    keys.append([entity, key])

        return keys
