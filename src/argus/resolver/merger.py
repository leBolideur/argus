from argus.models.entity import Entity
from argus.repositories.base_repository import BaseRepository


class Merger:
    def __init__(self, repo: BaseRepository):
        self.repo = repo

    def merge(self, origin: Entity, duplicate: Entity):
        print(f"origin: {origin}")
        print(f"duplicate: {duplicate}")

        for origin_key, origin_value in origin.properties.items():
            origin.properties.update(duplicate.properties)
            print(
                f"\nafter -- origin_value: {origin.properties[origin_key]} \tduplicate_value: {duplicate.properties[origin_key]}"
            )
            self.repo.reassign_relations(old_id=duplicate.id, new_id=origin.id)
            self.repo.delete_entity(duplicate.id)
