from pathlib import Path

import tomli

from orko.core.base import Dependency


def merge_deps(pyproject: dict) -> dict:
    project_deps = pyproject.get("project", {}).get("dependencies", {})
    orko_group = pyproject.get("tools", {}).get("orko", {})
    poetry_group = pyproject.get("tools", {}).get("poetry", {})
    project_opt_group = pyproject.get("project", {}).get("optional-dependencies", {})
    orko_deps = orko_group.get("dependencies", {})
    orko_opt_deps = orko_group.get("optional-dependencies", {})

    project_processed = []
    for p in project_deps:
        project_processed.append(Dependency(p))
    # project_processed = [Dependency(dep) for dep in project_deps]
    print(project_processed)



def load_pyproject(pyproject_path: str | Path = "pyproject.toml"):
    with open(pyproject_path, "rb") as pyproject_file:
        return tomli.load(pyproject_file)
