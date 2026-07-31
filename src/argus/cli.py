import typer
import json
from rich import print
from rich.console import Console
from typing import Annotated

from argus.orchestrator import Orchestrator
from argus.repositories.sqlite_repository import SQLiteRepository

err_console = Console(stderr=True)
app = typer.Typer()


@app.command()
def import_(
    source_path: Annotated[str, typer.Argument()],
    mapping_path: Annotated[str, typer.Option("-m")] = "mapping.toml",
):
    print(f"source: {source_path}\tmapping_path: {mapping_path}")
    orchestrator = Orchestrator(source_path, mapping_path, ":memory:")

    orchestrator.run()
    print(
        f"[bold green]Success![/bold green] {orchestrator.nb_entities} entities and {orchestrator.nb_relations} relations created!"
    )


@app.command()
def inspect(entity_id: Annotated[int, typer.Argument()]):
    repo = SQLiteRepository("argus.db")
    entity = repo.get_entity(entity_id)

    if entity is not None:
        print(f"Entity #{entity.id}")
        print(f"\tType: {entity.type}")
        print("\tProperties:")
        for key, value in entity.properties.items():
            print(f"\t\t{key}: {value}")
        relations = repo.get_relations_by_source_enriched(entity.id)

        if len(relations) > 0:
            print("\tRelationships:")
            for relation in relations:
                props = json.loads(relation["target_props"])
                print(
                    f"\t\t-> {relation['type']} -> {relation['target_type']} #{relation['target_id']}: {props}"
                )
    else:
        err_console.print(f"Entity {entity_id} not found!")

    repo.close()


@app.command()
def search(
    property: Annotated[str, typer.Option("-p")],
    value: Annotated[str, typer.Option("-v")],
):
    repo = SQLiteRepository("argus.db")

    try:
        entities = repo.search_entities_by_property(property, value)
        print(entities)
    except ValueError as e:
        err_console.print(f"[red bold]error: [/red bold]{e}")
    finally:
        repo.close()


if __name__ == "__main__":
    app()
