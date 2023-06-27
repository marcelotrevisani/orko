import rich_click as click
from orko.core.env import create_conda_env
from orko.core.process import get_deps
from orko.core.process import load_pyproject


@click.command(name="create")
@click.argument(
    "pyproject_file",
    type=click.Path(),
    required=True,
    help="Path to the pyproject.toml file.",
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
    # TODO: Need to add the verbose action which is going to control the logging level
    add_deps = add_deps or []
    pyproject = load_pyproject(pyproject_file)
    req_deps, opt_deps = get_deps(pyproject, tags)
    create_conda_env(
        name,
        conda_bin=conda_bin,
        conda_options=extra_args_conda,
        list_deps=add_deps + req_deps + opt_deps,
        conda_channels=channels,
    )
