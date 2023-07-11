import pytest
from orko.core.base import Dependency
from orko.core.process import get_run_deps
from orko.core.process import load_pyproject


def test_simple_build(tmp_pkg_folder, data_path):
    required_deps, optional_deps = get_run_deps(
        load_pyproject(data_path / "simple_pyproject.toml"), merge_deps=True
    )
    assert set(required_deps) == {
        Dependency("pytest"),
        Dependency(
            "setuptools-scm[toml]", version=">=6.2.3", conda_name="setuptools-scm"
        ),
        Dependency(
            "requests", version=">=2.23.0", python_version=">= '3.7'", platform="linux"
        ),
        Dependency("numba", python_version=">3.10"),
        Dependency("graphviz", conda_name="python-graphviz", python_version=">=3.7"),
        Dependency("pytest-xdist", version=">=1.0.0,<2.0.0", python_version=">= '3.7'"),
        Dependency("pytest-xdist", version=">=1.0.0", platform="linux"),
        Dependency("pytest-xdist", version=">=1.0.0,<2.0.0", platform="osx"),
        Dependency("python", version=">=3.10"),
    }


def test_strict_orko_build(tmp_pkg_folder, data_path):
    required_deps, optional_deps = get_run_deps(
        load_pyproject(data_path / "strict_orko.toml")
    )
    assert set(required_deps) == {
        Dependency(
            "requests", version=">=2.23.0", python_version=">= '3.7'", platform="linux"
        ),
        Dependency("numba", python_version=">3.10"),
        Dependency("graphviz", conda_name="python-graphviz", python_version=">=3.7"),
        Dependency("pytest-xdist", version=">=1.0.0", platform="linux"),
        Dependency("pytest-xdist", version=">=1.0.0,<2.0.0", platform="osx"),
        Dependency("python", version=">=3.10"),
    }


def test_dep_with_optional_pkg(data_path):
    required_deps, _ = get_run_deps(load_pyproject(data_path / "dep_modifier.toml"))
    assert required_deps == [
        Dependency(
            "setuptools-scm[toml]", conda_name="setuptools-scm", version=">=6.2.3"
        )
    ]


@pytest.mark.parametrize(
    "toml_file", ("optional_deps_as_dict.toml", "optional_deps_as_list.toml")
)
def test_get_optional_deps(data_path, toml_file):
    required_deps, optional_deps = get_run_deps(
        load_pyproject(data_path / toml_file), optional_deps_sections="*"
    )
    assert required_deps == []
    assert set(optional_deps) == {
        Dependency("pytest", platform="linux", version=">=6.2.3"),
        Dependency("pytest-xdist", platform="linux", python_version=">=3.7"),
    }
