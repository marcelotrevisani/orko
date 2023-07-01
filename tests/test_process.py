from orko.core.base import Dependency
from orko.core.process import replace_deps_with_orko_if_duplicated


def test_replace_deps_with_orko_if_duplicated():
    project_deps = [
        Dependency("pytest", version="1.2.3"),
        Dependency("pytest-xdist", platform="linux"),
        Dependency("flake8", version="2.3.4", platform="linux"),
        Dependency("graphviz", version="1.0.0"),
    ]
    orko_deps = [
        Dependency("abc"),
        Dependency("graphviz", conda_name="python-graphviz", version="2.0.0"),
        Dependency("pytest", version="3.0.0"),
    ]
    assert set(replace_deps_with_orko_if_duplicated(project_deps, orko_deps)) == {
        Dependency("pytest", version="3.0.0"),
        Dependency("pytest-xdist", platform="linux"),
        Dependency("flake8", version="2.3.4", platform="linux"),
        Dependency("graphviz", version="2.0.0", conda_name="python-graphviz"),
    }
