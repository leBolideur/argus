from argus.connectors.csv_connector import CSVConnector


def test_csv_connector():
    connector = CSVConnector()
    records = connector.read("tests/fixtures/employees.csv")

    assert len(records) == 12
