from abc import ABC, abstractmethod

from argus.models.record import Record


class BaseConnector(ABC):
    @abstractmethod
    def read(self, path: str) -> list[Record]:
        pass
