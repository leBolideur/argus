# Argus

> Transform disconnected data into connected knowledge.

[![Python](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-MVP-green.svg)](#roadmap)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-orange.svg)](https://docs.astral.sh/ruff/)

## Overview

Argus is a **generic Knowledge Graph Engine** that transforms heterogeneous, disconnected data (CSV) into a connected graph of knowledge.

The core principle: **the engine knows nothing about your domain**. It doesn't know what a Person, a Company, or an Email is. It only manipulates three concepts:

- **Entity** — a node with a type and properties
- **Relationship** — a directed edge between two entities, with its own properties
- **Property** — a key-value pair stored as JSON

Everything else — what entity types exist, how columns map to entities, which relationships connect them — is defined by an explicit **ontology** (a TOML mapping file), not hardcoded in the engine.

## Features

- **Generic engine** — No domain knowledge baked in. Define your ontology in TOML.
- **Declarative mapping** — Column-to-entity mapping with explicit relationship definitions.
- **SQLite storage** — Zero-install, portable, queryable via `json_extract()`.
- **Modern CLI** — Built with Typer + Rich for a clean, interactive experience.
- **Typed Python** — Strict type hints, MyPy and Ruff enforced via pre-commit hooks.
- **Extensible architecture** — Abstract base classes for connectors and repositories.

## Architecture

```
CSV File │ ▼ Connector ──► Record (source, fields) │ ▼ Mapper ──► Entity (type, properties) │ ▼ Storage (SQLite) ──► IDs assigned │ ▼ RelationshipBuilder ──► Relationship (type, source, target) │ ▼ Storage (SQLite) │ ▼ CLI (inspect, search)
```

### Design Patterns

| Pattern | Where | Why |
|---------|-------|-----|
| Abstract Base Class | `BaseConnector`, `BaseRepository` | Swappable implementations |
| Repository | `SQLiteRepository` | Encapsulates data access logic |
| Facade / Orchestrator | `Orchestrator` | Coordinates the full pipeline |
| Dataclass | `Record`, `Entity`, `Relationship` | Pure data models, no business logic |
| Pipeline | End-to-end flow | Clear separation of stages |

## Quick Start

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
git clone https://github.com/leBolideur/argus.git
cd argus
uv sync --dev
```

### Usage

**Import a CSV file and build the knowledge graph:**

```bash
uv run argus import tests/fixtures/employees.csv -m mapping.toml
```

Output:
```
source: tests/fixtures/employees.csv mapping_path: mapping.toml
Success! 40 entities and 16 relations created!
```

**Inspect an entity and its relationships:**

```bash
uv run argus inspect 1
```

Output:
```
Entity #1
  Type: Person
  Properties:
    first_name: John
    last_name: Doe
  Relationships:
    -> WORK_FOR -> Company #9: {'name': 'OpenAI'}
    -> HAS_EMAIL -> Email #17: {'value': 'john@openai.com'}
```

**Search entities by property:**

```bash
uv run argus search -p value -v john@openai.com
```

### Defining Your Ontology

Create a `mapping.toml` file that describes how your CSV columns map to entities and relationships:

Map CSV columns to entity types and properties
```toml
[columns.first_name]
entity = "Person"
property = "first_name"

[columns.email]
entity = "Email"
property = "value"

[columns.company]
entity = "Company"
property = "name"
```

Define relationships between entity types
```toml
[[relationships]]
type = "WORKS_FOR"
source = "Person"
target = "Company"

[[relationships]]
type = "HAS_EMAIL"
source = "Person"
target = "Email"
```

## Project Structure

```text
argus/
├── src/argus/
    ├── cli.py              # Typer CLI (import, inspect, search)
    ├── orchestrator.py     # Pipeline coordinator
    ├── mapper.py           # Record → Entity transformation
    ├── builder.py          # Entity → Relationship builder
    ├── models/
    ├── connectors/
    └── repositories/
├── tests/
├── pyproject.toml
└── README.md
```

## Tech Stack

| Tool | Role |
|------|------|
| [Python 3.14+](https://www.python.org/) | Core language |
| [uv](https://docs.astral.sh/uv/) | Dependency management |
| [Typer](https://typer.tiangolo.com/) | CLI framework |
| [Rich](https://rich.readthedocs.io/) | Terminal formatting |
| [SQLite](https://www.sqlite.org/) | Storage (stdlib `sqlite3`) |
| [tomllib](https://docs.python.org/3/library/tomllib.html) | Mapping parsing (stdlib) |
| [Ruff](https://docs.astral.sh/ruff/) | Linting & formatting |
| [MyPy](https://mypy-lang.org/) | Static type checking |
| [pytest](https://docs.pytest.org/) | Testing |
| [pre-commit](https://pre-commit.com/) | Git hooks |

## Roadmap

| Version | Status | Features |
|---------|--------|----------|
| `v0.1.0` | ✅ Released | MVP — Single CSV import, TOML mapping, CLI, SQLite storage |
| `v0.2.0` | 🚧 Next | Entity Resolution — Deduplication (Transformers → Comparers → Linkers) |
| `v0.3.0` | ⏳ Planned | Multi-file import — Cross-source knowledge graph merging |
| `v0.4.0` | ⏳ Planned | Query Engine — Multi-hop traversals, advanced filtering |
| `v0.5.0` | ⏳ Planned | FastAPI — REST API to expose Argus over HTTP |

See the [open issues](https://github.com/leBolideur/argus/issues) and [GitHub Projects board](https://github.com/leBolideur/argus/projects) for detailed tracking.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
