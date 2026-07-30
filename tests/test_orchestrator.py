from argus.orchestrator import Orchestrator


def test_full_pipeline():
    orchestrator = Orchestrator(
        "tests/fixtures/employees.csv", "tests/fixtures/mapping.toml", ":memory:"
    )
    orchestrator.run()

    assert orchestrator.nb_entities == 40
    assert orchestrator.nb_relations == 16
