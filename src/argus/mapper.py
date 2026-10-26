# from collections import defaultdict
# import tomllib
#
# from argus.models.entity import Entity
# from argus.models.record import Record
#
#
# class Mapper:
#     def make_grouped_entities(
#         self, path: str, records: list[Record]
#     ) -> list[list[Entity]]:
#         with open(path, "rb") as file:
#             mapping = tomllib.load(file)
#
#         entities = []
#         for record in records:
#             acc: dict = defaultdict(dict)
#             for key, value in record.fields.items():
#                 if key in mapping["columns"]:
#                     entity_type = mapping["columns"][key]["entity"]
#                     entity_property = mapping["columns"][key]["property"]
#                     acc[entity_type] = {**acc[entity_type], entity_property: value}
#
#             group = []
#             for key, value in acc.items():
#                 entity = Entity(
#                     type=key,
#                     properties=value,
#                 )
#
#                 group.append(entity)
#             entities.append(group)
#         return entities
