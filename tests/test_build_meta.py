import shutil

from pip._internal.cli.main import main

def test_simple_build(tmp_pkg_folder, data_path):
    shutil.copyfile(data_path / "simple_pyproject.toml", tmp_pkg_folder / "pyproject.toml")
    main(["install", "-q", "build", str(tmp_pkg_folder), "--no-build-isolation"])
    pass