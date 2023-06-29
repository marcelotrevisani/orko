import subprocess
from pathlib import Path


def create_conda_env(
    env_file: str | Path,
    *,
    conda_bin: str | Path = "conda",
    conda_options: str = "",
):
    conda_cmd = [
        str(conda_bin),
        "env",
        "create",
        "-f",
        str(env_file),
    ]
    if conda_options:
        conda_cmd.append(conda_options)
    subprocess.run(
        " ".join(conda_cmd),
        shell=True,
        check=True,
    )


def run_conda_build(
    conda_bin: str | Path = "conda",
    conda_channels: list[str] | None = None,
    req_build: list[str] | None = None,
    req_host: list[str] | None = None,
    req_run: list[str] | None = None,
    requires_test: list[str] | None = None,
):
    pass
