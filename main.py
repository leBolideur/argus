from argus.connectors.csv_connector import CSVConnector


def main():
    print("Hello from argus!")

    # db = SQLiteRepository("argus.db")
    # entity = Entity(properties={"name": "Max"}, type="PERSON")
    # inserted = db.insert_entity(entity)
    # print(inserted)

    # relationship = Relationship(type="FRIEND", source=1, target=1, properties={})
    # inserted = db.insert_relationship(relationship)
    # print(inserted)

    # get = db.get_entity(1)
    # print(get)

    # relationships = db.get_by_source(1)
    # for rel in relationships:
    #     print(rel)

    # db.close()

    connector = CSVConnector()
    records = connector.read("tests/fixtures/employees.csv")
    for record in records:
        print(record)


if __name__ == "__main__":
    main()
