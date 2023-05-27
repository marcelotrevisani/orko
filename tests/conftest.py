from pathlib import Path

import pytest


@pytest.fixture(scope="function")
def tmp_pkg_folder(tmp_path):
    foo_pkg_root_dir = tmp_path / "pkg_test"
    foo_pkg_root_dir.mkdir()
    setup_py = foo_pkg_root_dir / "setup.py"
    setup_py.write_text("from setuptools import setup\nsetup(name='orko_foo_test')")
    orko_test_dir = foo_pkg_root_dir / "orko_foo_test"
    orko_test_dir.mkdir()
    return foo_pkg_root_dir

@pytest.fixture
def data_path():
    return Path(__file__).parent / "data"