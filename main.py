from argus.connectors.csv_connector import CSVConnector
from argus.mapper import Mapper


def main():
    print("Hello from argus!")

    connector = CSVConnector()
    records = connector.read("tests/fixtures/employees.csv")

    mapper = Mapper()
    entities = mapper.make_grouped_entities("tests/fixtures/mapping.toml", records)
    for entity in entities:
        print(entity)
        print()


if __name__ == "__main__":
    main()
