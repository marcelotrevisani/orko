from functools import singledispatch
from pathlib import Path
from typing import List

import tomli
from orko.core.base import Dependency


def get_deps(pyproject: dict) -> tuple[list[Dependency], list[Dependency]]:
    project_deps = pyproject.get("project", {}).get("dependencies", {})
    orko_group = pyproject.get("tools", {}).get("orko", {})
    project_opt_group = pyproject.get("project", {}).get("optional-dependencies", {})
    orko_deps = orko_group.get("dependencies", {})
    orko_opt_deps = orko_group.get("optional-dependencies", {})
    is_strict_orko = orko_group.get("config", {}).get("strict_orko", False)
    all_req_deps = []
    if not is_strict_orko:
        for p in project_deps:
            all_req_deps.extend(convert_to_dependency_obj(p))
    all_req_deps.extend(convert_to_dependency_obj(orko_deps))

    all_opt_deps = []
    if not is_strict_orko:
        for p in project_opt_group:
            all_req_deps.extend(convert_to_dependency_obj(p))
    all_req_deps.extend(convert_to_dependency_obj(orko_opt_deps))
    return all_req_deps, all_opt_deps


def load_pyproject(pyproject_path: str | Path = "pyproject.toml"):
    with open(pyproject_path, "rb") as pyproject_file:
        return tomli.load(pyproject_file)


@singledispatch
def convert_to_dependency_obj(pkg: str) -> List[Dependency]:
    return [Dependency(pkg)]


@convert_to_dependency_obj.register
def __convert_to_dependency_obj_dict(pkg: dict) -> List[Dependency]:
    result = []
    for name, params in pkg.items():
        params = params or {}
        if isinstance(params, list):
            for param_value in params:
                result.extend(convert_to_dependency_obj({name: param_value}))
        else:
            result.append(Dependency(name, **params))
    return result
