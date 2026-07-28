from argus.orchestrator import Orchestrator


def test_full_pipeline():
    orchestrator = Orchestrator(
        "tests/fixtures/employees.csv", "tests/fixtures/mapping.toml", ":memory:"
    )
    orchestrator.run()
