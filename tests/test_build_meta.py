from orko.core.process import merge_deps, load_pyproject


def test_simple_build(tmp_pkg_folder, data_path):
    merge_deps(load_pyproject(data_path / "simple_pyproject.toml"))
    # shutil.copyfile(data_path / "simple_pyproject.toml", tmp_pkg_folder / "pyproject.toml")
    # with open(tmp_pkg_folder / "pyproject.toml", "rb") as f:
    #     p = tomli.load(f)
    # print(p)
    # main(["install", "-q", "build", str(tmp_pkg_folder), "--no-build-isolation"])
