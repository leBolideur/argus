from argus.orchestrator import Orchestrator


def main():
    print("Hello from argus!")

    orchestrator = Orchestrator(
        "tests/fixtures/employees.csv", "tests/fixtures/mapping.toml", "argus.db"
    )

    orchestrator.run()


if __name__ == "__main__":
    main()
