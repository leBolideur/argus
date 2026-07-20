from argus.models.record import Record
from argus.models.entity import Entity
from argus.models.relationship import Relationship


def test_imports():
    assert Record is not None
    assert Entity is not None
    assert Relationship is not None


def test_mypy():
    _ = Record(source="file.csv", fields={})
    _ = Entity(id=1, type="Person", properties={})
    _ = Relationship(id=1, type="TEST", source=1, target=2, properties={})
    assert True
