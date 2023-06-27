import rich_click as click


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
def cli_create_env():
    pass
