import logging
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
    logging.debug(f"Extracted dependencies from {'.'.join(path_key)}: {all_deps}")
    return all_deps


def replace_deps_with_orko_if_duplicated(
    project_deps: List[Dependency], orko_deps: List[Dependency]
) -> List[Dependency]:
    normalised_deps = []
    for project_pkg in project_deps:
        find_pkg = False
        for orko_pkg in orko_deps:
            if project_pkg.name == orko_pkg.name:
                logging.info(f"Replacing {project_pkg.name} with {orko_pkg.name}")
                normalised_deps.append(orko_pkg)
                find_pkg = True
        if not find_pkg:
            normalised_deps.append(project_pkg)
    normalised_deps = list(set(normalised_deps))
    logging.debug(
        f"Dependency replace. Old: {project_deps}, Replaced by: {normalised_deps}"
    )
    return normalised_deps


def get_run_deps(
    pyproject: dict,
    optional_deps_sections: list[str] | str = "",
    merge_deps: bool = False,
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
        if not merge_deps:
            project_deps = replace_deps_with_orko_if_duplicated(project_deps, orko_deps)

    logging.debug(f"[project] deps: {project_deps}")
    if optional_deps_sections == "*" or "*" in optional_deps_sections:
        opt_deps_project_sections = list(
            pyproject.get("project", {}).get("optional-dependencies", {}).keys()
        )
        opt_deps_orko_sections = list(
            pyproject.get("tools", {})
            .get("orko", {})
            .get("optional-dependencies", {})
            .keys()
        )
    else:
        opt_deps_project_sections = optional_deps_sections or []
        opt_deps_orko_sections = optional_deps_sections or []

    all_opt_deps_project = []
    if not is_strict_orko:
        for k in opt_deps_project_sections:
            all_opt_deps_project.extend(
                extract_specific_deps(
                    pyproject, ["project", "optional-dependencies", k]
                )
            )

    all_opt_deps_orko = []
    for k in opt_deps_orko_sections:
        all_opt_deps_orko.extend(
            extract_specific_deps(
                pyproject, ["tools", "orko", "optional-dependencies", k]
            )
        )
    logging.debug(f"[orko.optional-dependencies]: {all_opt_deps_orko}")
    logging.debug(f"[project.optional-dependencies]: {all_opt_deps_project}")
    all_opt_deps = all_opt_deps_orko
    if merge_deps:
        all_opt_deps.extend(all_opt_deps_project)
    else:
        all_opt_deps.extend(
            replace_deps_with_orko_if_duplicated(
                all_opt_deps_project, all_opt_deps_orko
            )
        )
    logging.debug(f"Optional dependencies to install: {all_opt_deps}")
    all_required_deps = project_deps + orko_deps
    logging.debug(f"Required deps to install: {all_required_deps}")

    if requires_python := pyproject.get("project", {}).get("requires-python", None):
        all_required_deps.append(Dependency("python", version=requires_python))

    return all_required_deps, all_opt_deps


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


def get_all_build_deps(pyproject):
    build_deps = pyproject.get("build-system", {}).get("requires", [])
    return [Dependency(d) for d in build_deps if d]
