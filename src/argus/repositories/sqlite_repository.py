import json
import re
import sqlite3
from typing import Any

from argus.models.entity import Entity, EntityType
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
            """CREATE TABLE IF NOT EXISTS entity_types(
                id integer primary key autoincrement not null,
                name varchar(255) not null unique
                )"""
        )

        for type in EntityType:
            self.conn.cursor().execute(
                "INSERT OR IGNORE INTO entity_types(name) VALUES(:name)",
                {"name": type},
            )
        self.conn.commit()

        self.conn.cursor().execute(
            """CREATE TABLE IF NOT EXISTS entities(
                id integer primary key autoincrement not null,
                source varchar(255) not null,
                line integer not null,
                type integer not null,
                trusted bool not null,
                properties text not null,
                FOREIGN KEY(type) REFERENCES entity_types(id)
                )"""
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
        type = self.conn.cursor().execute(
            "SELECT id FROM entity_types WHERE name = :name", {"name": entity.type}
        )
        type_id = type.fetchone()[0]

        properties = json.dumps(entity.properties)
        query = self.conn.cursor().execute(
            "INSERT INTO entities(source, line, type, trusted, properties) VALUES(:source, :line, :type, :trusted, :properties) RETURNING id",
            {
                "source": entity.source,
                "line": entity.line,
                "properties": properties,
                "type": type_id,
                "trusted": entity.trusted,
            },
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
            """SELECT e.id, e.source, e.line, e.properties, e.trusted, t.name as type
            FROM entities e
            INNER JOIN entity_types t ON t.id = e.type
            WHERE e.id = :id""",
            {"id": id},
        )
        entity = query.fetchone()

        if entity is None:
            return None

        return Entity(
            id=entity["id"],
            source=entity["source"],
            line=entity["line"],
            type=entity["type"],
            trusted=True if entity["trusted"] == 1 else False,
            properties=json.loads(entity["properties"]),
        )

    def get_all_entities(self) -> list[Entity]:
        # TODO: Get type name in entity_types
        query = self.conn.cursor().execute(
            "SELECT e.*, t.name as type_name FROM entities e INNER JOIN entity_types t ON e.type = t.id"
        )
        rows = query.fetchall()
        return [
            Entity(
                id=entity["id"],
                source=entity["source"],
                line=entity["line"],
                type=entity["type_name"],
                trusted=entity["trusted"],
                properties=json.loads(entity["properties"]),
            )
            for entity in rows
        ]

    def get_all_entities_by_type(self, type: str) -> list[Entity]:
        query = self.conn.cursor().execute(
            """SELECT e.id, e.source, e.line, e.type, e.properties, e.trusted, t.name as type_name, t.id
            FROM entities e INNER JOIN entity_types t ON e.type = t.id
            WHERE t.name = :type""",
            {"type": type},
        )
        rows = query.fetchall()
        return [
            Entity(
                id=row["id"],
                source=row["source"],
                line=row["line"],
                type=row["type_name"],
                trusted=True if row["trusted"] == 1 else False,
                properties=json.loads(row["properties"]),
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
                id=row["id"],
                source=row["source"],
                line=row["line"],
                type=row["type"],
                trusted=row["trusted"],
                properties=json.loads(row["properties"]),
            )
            for row in results
        ]

        return entities

    def close(self):
        self.conn.close()
