# from argus.connectors.csv_connector import CSVConnector
# from argus.mapper import Mapper
#
#
# def test_mapper():
#     connector = CSVConnector()
#     records = connector.read("tests/fixtures/employees.csv")
#
#     mapper = Mapper()
#     grouped_entities = mapper.make_grouped_entities(
#         "tests/fixtures/mapping.toml", records
#     )
#
#     assert len(grouped_entities) == 8
#     for grouped_entity in grouped_entities:
#         for entity in grouped_entity:
#             if entity.type == "Person":
#                 assert (
#                     "first_name" in entity.properties
#                     and "last_name" in entity.properties
#                 )
