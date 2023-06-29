import tempfile

import rich_click as click
import yaml
from orko.core.base import Dependency
from orko.core.env import create_conda_env
from orko.core.process import get_deps
from orko.core.process import load_pyproject


@click.command(name="create")
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
@click.option("--verbose", "-v", count=True, help="Verbose mode.")
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
):
    """CLI to create environments looking for pyproject.toml"""
    # TODO: Need to add the verbose action which is going to control the logging level
    add_deps = add_deps or []
    add_deps = [Dependency(d) for d in add_deps if d]
    pyproject = load_pyproject(pyproject_file)
    req_deps, opt_deps = get_deps(pyproject, optional)
    if requires_python := pyproject.get("projecy", {}).get("requires-python", None):
        req_deps.append(Dependency("python", version=requires_python))

    build_deps = pyproject.get("build-system", {}).get("requires", [])
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
        env_file.write(yaml.dump(env_content).encode("utf-8"))
        env_file.flush()
        create_conda_env(
            env_file.name,
            conda_bin=conda_bin,
            conda_options=extra_args_conda,
        )
