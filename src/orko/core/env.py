import subprocess
from pathlib import Path


def create_conda_env(
    env_name: str,
    *,
    conda_bin: str | Path = "conda",
    conda_options: str = "",
    list_deps: list[str] | None = None,
    conda_channels: list[str] | None = None,
):
    list_deps = list_deps or []
    channels_cmd = "-c ".join(conda_channels) if conda_channels else ""
    subprocess.run(
        [
            str(conda_bin),
            "env",
            "create",
            "-n",
            env_name,
            " ".join(list_deps),
            channels_cmd,
            conda_options,
        ],
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
