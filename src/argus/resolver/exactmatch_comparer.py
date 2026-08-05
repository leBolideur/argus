from argus.models.entity import Entity


class ExactMatchComparer:
    def _normalize(self, input: str | None) -> str:
        return "" if input is None else input.lower().strip()

    def get_key(self, entity: Entity, prop_key: str) -> str:
        return self._normalize(entity.properties[prop_key])
