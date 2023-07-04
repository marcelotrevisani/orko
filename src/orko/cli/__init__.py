import logging
import tempfile

import rich_click as click
import yaml
from orko.core.base import Dependency
from orko.core.env import create_conda_env
from orko.core.process import get_deps
from orko.core.process import load_pyproject


LOGGER = logging.getLogger(__name__)


@click.group(name="orko", help="Orko CLI")
def orko_cli():
    ...


@orko_cli.command(name="create")
@click.argument(
    "pyproject_file",
    type=click.Path(),
    required=True,
)
@click.option("--name", "-n", type=str, required=True, help="Environment name")
@click.option("--channels", "-c", multiple=True, help="Conda channels to use")
@click.option(
    "--add-deps",
    "-a",
    multiple=True,
    help="Add new dependencies when creating the environment",
)
@click.option("--verbose", "-v", count=True, help="Verbose mode.", default=0)
@click.option(
    "--optional",
    "-o",
    multiple=True,
    help="Tags that orko will look for when creating the environment."
    " If you want to install all the optional dependencies"
    " please specify `--tags=*`",
)
@click.option(
    "--conda-bin",
    default="conda",
    help="Conda executable path file, it also accepts mamba/micromamba.",
    required=False,
)
@click.option(
    "--extra-args-conda",
    help="Extra arguments to be passed to the `conda create`.",
    type=str,
)
@click.option(
    "--add-build-deps",
    help="Add build dependencies [build-system]requires.",
    required=False,
    is_flag=True,
    default=False,
    show_default=True,
)
@click.option(
    "--merge-deps",
    help="The default behaviour is to replace any dependency in [project]"
    " with the dependency specified in orko. If this flag is active"
    " orko is going to add all deps in project and in orko.",
    is_flag=True,
    default=False,
    show_default=False,
    required=False,
)
def cli_create_env(
    pyproject_file,
    name,
    channels,
    add_deps,
    verbose,
    optional,
    conda_bin,
    extra_args_conda,
    add_build_deps,
    merge_deps,
):
    """CLI to create environments looking for pyproject.toml"""
    set_logging_level(verbose)

    add_deps = add_deps or []
    add_deps = [Dependency(d) for d in add_deps if d]
    pyproject = load_pyproject(pyproject_file)
    req_deps, opt_deps = get_deps(pyproject, optional, merge_deps=merge_deps)
    if requires_python := pyproject.get("projecy", {}).get("requires-python", None):
        req_deps.append(Dependency("python", version=requires_python))

    build_deps = pyproject.get("build-system", {}).get("requires", [])
    build_deps = [Dependency(d) for d in build_deps if d]
    if add_build_deps and build_deps:
        opt_deps.extend(build_deps)
    all_deps = [d.conda_dep_style for d in req_deps + opt_deps + add_deps if d]

    env_content = {
        "name": name,
    }
    if channels:
        env_content["channels"] = [channels] if isinstance(channels, str) else channels
    env_content["dependencies"] = all_deps

    with tempfile.NamedTemporaryFile(prefix="environment-", suffix=".yml") as env_file:
        yaml_env = yaml.dump(env_content).encode("utf-8")
        LOGGER.debug(f"environment.yaml:\n{yaml_env}")
        env_file.write(yaml_env)
        env_file.flush()
        create_conda_env(
            env_file.name,
            conda_bin=conda_bin,
            conda_options=extra_args_conda,
        )


def set_logging_level(verbose):
    match verbose:
        case 1:
            LOGGER.setLevel(logging.INFO)
        case 2:
            LOGGER.setLevel(logging.ERROR)
        case _ if verbose >= 3:
            LOGGER.setLevel(logging.CRITICAL)
        case _:
            LOGGER.setLevel(logging.NOTSET)


if __name__ == "__main__":
    orko_cli()
