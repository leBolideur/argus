from argus.models.record import Record
from argus.models.entity import Entity, EntityType
from argus.models.relationship import Relationship


def test_imports():
    assert Record is not None
    assert Entity is not None
    assert Relationship is not None


def test_mypy():
    _ = Record(source="file.csv", line=0, fields={})
    _ = Entity(id=1, source="file.csv", line=0, type=EntityType.PERSON, properties={})
    _ = Relationship(id=1, type="TEST", source=1, target=2, properties={})
    assert True
