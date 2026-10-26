import sqlite3

import pytest

from argus.models.entity import Entity, EntityType
from argus.models.relationship import Relationship
from argus.repositories.sqlite_repository import SQLiteRepository


@pytest.fixture
def repo():
    repo = SQLiteRepository(":memory:")
    yield repo
    repo.close()


def test_entities(repo: SQLiteRepository):
    entity = Entity(
        type=EntityType.PERSON,
        source="test.csv",
        line=0,
        properties={
            "firstname": "foo",
            "lastname": "bar",
        },
    )
    entity_id = repo.insert_entity(entity)
    assert entity_id == 1

    get_entity = repo.get_entity(entity_id)
    assert get_entity is not None
    assert get_entity.id == 1
    assert get_entity.properties == {"firstname": "foo", "lastname": "bar"}
    assert get_entity.type == "PERSON"


def test_relationships(repo: SQLiteRepository):
    entity1 = repo.insert_entity(
        Entity(
            type=EntityType.PERSON, source="test", line=0, properties={"name": "Bob"}
        )
    )
    entity2 = repo.insert_entity(
        Entity(
            type=EntityType.UNKNOWN,
            source="test",
            line=1,
            properties={"name": "proton"},
        )
    )

    relationship = Relationship(
        type="WORK_AT",
        source=entity1,
        target=entity2,
        properties={
            "firstname": "foo",
            "lastname": "bar",
        },
    )

    relationship_id = repo.insert_relationship(relationship)
    assert relationship_id == 1

    get_relationships = repo.get_relations_by_source(entity1)
    assert len(get_relationships) == 1


def test_fk_constraint(repo: SQLiteRepository):
    with pytest.raises(sqlite3.IntegrityError):
        repo.insert_relationship(
            Relationship(type="BUG", source=4, target=5, properties={})
        )
