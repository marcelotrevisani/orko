from orko.core.base import Dependency


def test_dependency_creation():
    dep = Dependency(
        "pytest-xdist >=1.0.0,<2.0.0; python_version >= '3.7'",
        conda_name="conda-pytest-xdist",
    )
    assert dep.name == "pytest-xdist"
    assert str(dep.specifier) == "<2.0.0,>=1.0.0"
    assert str(dep.marker) == 'python_version >= "3.7"'
    assert dep.conda_name == "conda-pytest-xdist"


def test_creation_empty_conda_name():
    dep = Dependency(
        "pytest-xdist >=1.0.0,<2.0.0; python_version >= '3.7'",
    )
    assert dep.name == "pytest-xdist"
    assert str(dep.specifier) == "<2.0.0,>=1.0.0"
    assert str(dep.marker) == 'python_version >= "3.7"'
    assert dep.conda_name == "pytest-xdist"


def test_create_using_fields_parameters():
    dep = Dependency(
        "pytest",
        conda_name="pytest-conda",
        version=">3.0.0,<=5.2.3",
        platform="osx",
        python_version="3.10",
    )
    assert dep.name == "pytest"
    assert dep.conda_name == "pytest-conda"
    assert str(dep.specifier) == "<=5.2.3,>3.0.0"
    assert str(dep.marker) == 'os_name == "osx" and python_version == "3.10"'
    assert dep.conda_dep_style == "pytest-conda  # [osx and ((py==310))]"
