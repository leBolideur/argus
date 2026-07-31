from typing import Any
import re
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

    def get_all_entities(self) -> list[Entity]:
        query = self.conn.cursor().execute("SELECT * FROM entities")
        entities = query.fetchall()
        return entities

    def get_all_entities_by_type(self, type: str) -> list[Entity]:
        query = self.conn.cursor().execute(
            "SELECT * FROM entities WHERE type = :type", {"type": type}
        )
        rows = query.fetchall()
        return [
            Entity(
                id=row["id"], type=row["type"], properties=json.loads(row["properties"])
            )
            for row in rows
        ]

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

    def insert_batch_relations(
        self, relations: list[Relationship]
    ) -> list[Relationship]:
        for relation in relations:
            relation_id = self.insert_relationship(relation)
            relation.id = relation_id

        return relations

    def get_relations_by_source(self, source: int) -> list[Relationship]:
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

    def get_relations_by_source_enriched(self, source: int) -> list[Any]:
        query = self.conn.cursor().execute(
            """SELECT
                 r.id, r.type, r.source, r.target,
                 s.id as source_id, s.type as source_type, s.properties as source_props,
                 t.id as target_id, t.type as target_type, t.properties as target_props
                 FROM relationships r
                 INNER JOIN entities s ON r.source = s.id
                 INNER JOIN entities t ON r.target = t.id
                 WHERE r.source = :source""",
            {"source": source},
        )
        rows = query.fetchall()
        return rows

    def search_entities_by_property(self, property: str, value: str) -> list[Entity]:
        safe_property = re.match("^[a-zA-Z0-9-_.]+$", property)
        if not safe_property:
            raise ValueError(f"Invalid property name: {property}")

        query = self.conn.cursor().execute(
            "SELECT * FROM entities WHERE json_extract(properties, :property) = :value",
            {"property": f"$.{safe_property.string}", "value": value},
        )
        results = query.fetchall()

        entities = [
            Entity(
                id=row["id"], type=row["type"], properties=json.loads(row["properties"])
            )
            for row in results
        ]

        return entities

    def close(self):
        self.conn.close()
