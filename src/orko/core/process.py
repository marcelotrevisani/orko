from functools import singledispatch
from pathlib import Path
from typing import List

import tomli
from orko.core.base import Dependency


def extract_specific_deps(
    pyproject: dict, path_key: list | None = None
) -> list[Dependency]:
    path_key = path_key or []
    group_project = pyproject
    for k in path_key:
        group_project = group_project.get(k, {})

    all_deps = []
    if isinstance(group_project, list):
        for dep in group_project:
            all_deps.extend(convert_to_dependency_obj(dep))
    else:
        all_deps.extend(convert_to_dependency_obj(group_project))
    return all_deps


def get_deps(
    pyproject: dict, optional_deps_sections: list[str] | None = None
) -> tuple[list[Dependency], list[Dependency]]:
    is_strict_orko = (
        pyproject.get("tools", {})
        .get("orko", {})
        .get("config", {})
        .get("strict_orko", False)
    )
    orko_deps = extract_specific_deps(pyproject, ["tools", "orko", "dependencies"])
    if is_strict_orko:
        project_deps = []
    else:
        project_deps = extract_specific_deps(pyproject, ["project", "dependencies"])

    if optional_deps_sections is not None and len(optional_deps_sections) > 0:
        opt_deps_project_sections = optional_deps_sections or []
        opt_deps_orko_sections = optional_deps_sections or []
    else:
        opt_deps_project_sections = list(
            pyproject.get("project", {}).get("optional-dependencies", {}).keys()
        )
        opt_deps_orko_sections = list(
            pyproject.get("tools", {})
            .get("orko", {})
            .get("optional-dependencies", {})
            .keys()
        )

    all_opt_deps = []
    if not is_strict_orko:
        for k in opt_deps_project_sections:
            all_opt_deps.extend(
                extract_specific_deps(
                    pyproject, ["project", "optional-dependencies", k]
                )
            )

    for k in opt_deps_orko_sections:
        all_opt_deps.extend(
            extract_specific_deps(
                pyproject, ["tools", "orko", "optional-dependencies", k]
            )
        )

    return project_deps + orko_deps, all_opt_deps


def load_pyproject(pyproject_path: str | Path = "pyproject.toml"):
    with open(pyproject_path, "rb") as pyproject_file:
        return tomli.load(pyproject_file)


@singledispatch
def convert_to_dependency_obj(pkg: str, tag: str = "required") -> List[Dependency]:
    return [Dependency(pkg, tag=tag)]


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
