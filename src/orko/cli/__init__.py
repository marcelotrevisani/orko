import tempfile

import rich_click as click
import yaml
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
    "--tags",
    "-t",
    multiple=True,
    help="Tags that orko will look for when creating the environment",
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
def cli_create_env(
    pyproject_file, name, channels, add_deps, verbose, tags, conda_bin, extra_args_conda
):
    """CLI to create environments looking for pyproject.toml"""
    # TODO: Need to add the verbose action which is going to control the logging level
    add_deps = add_deps or []
    pyproject = load_pyproject(pyproject_file)
    req_deps, opt_deps = get_deps(pyproject, tags)
    all_deps = [d.conda_dep_style for d in req_deps + opt_deps if d]

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
