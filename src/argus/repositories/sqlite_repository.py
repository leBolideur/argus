import sqlite3
import json

from argus.models.entity import Entity
from argus.models.relationship import Relationship
from argus.repositories.base_repository import BaseRepository


class SQLiteRepository(BaseRepository):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row

        self.create_tables()

    def create_tables(self):
        self.conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS entities(id integer primary key autoincrement not null, type varchar(255) not null, properties text not null)"
        )

        self.conn.cursor().execute(
            """CREATE TABLE IF NOT EXISTS relationships(
            id integer primary key autoincrement not null,
            type varchar(255),
            source integer not null,
            target integer not null,
            properties text not null,
            FOREIGN KEY(source) REFERENCES entities(id),
            FOREIGN KEY(target) REFERENCES entities(id)
            )"""
        )

    def insert_entity(self, entity: Entity) -> int:
        properties = json.dumps(entity.properties)
        query = self.conn.cursor().execute(
            "INSERT INTO entities(properties, type) VALUES(:properties, :type) RETURNING id",
            {"properties": properties, "type": entity.type},
        )
        row = query.fetchone()
        self.conn.commit()
        return row["id"]

    def insert_batch_entities(self, batch: list[list[Entity]]) -> list[list[Entity]]:
        for entities_list in batch:
            for entity in entities_list:
                entity_id = self.insert_entity(entity)
                entity.id = entity_id

        return batch

    def get_entity(self, id: int) -> Entity | None:
        query = self.conn.cursor().execute(
            "SELECT * FROM entities WHERE id = :id", {"id": id}
        )
        entity = query.fetchone()

        if entity is None:
            return None

        return Entity(
            id=entity["id"],
            type=entity["type"],
            properties=json.loads(entity["properties"]),
        )

    def insert_relationship(self, relationship: Relationship) -> int:
        properties = json.dumps(relationship.properties)
        query = self.conn.cursor().execute(
            "INSERT INTO relationships(properties, source, target, type) VALUES(:properties, :source, :target, :type) RETURNING id",
            {
                "properties": properties,
                "source": relationship.source,
                "target": relationship.target,
                "type": relationship.type,
            },
        )
        row = query.fetchone()
        self.conn.commit()
        return row["id"]

    def get_by_source(self, source: int) -> list[Relationship]:
        query = self.conn.cursor().execute(
            "SELECT * FROM relationships WHERE source = :source", {"source": source}
        )
        rows = query.fetchall()

        relationships = [
            Relationship(
                id=row["id"],
                type=row["type"],
                source=row["source"],
                target=row["target"],
                properties=json.loads(row["properties"]),
            )
            for row in rows
        ]

        return relationships

    def close(self):
        self.conn.close()
