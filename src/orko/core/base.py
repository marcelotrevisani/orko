import re

from packaging.requirements import Requirement
from packaging.specifiers import InvalidSpecifier
from packaging.specifiers import SpecifierSet


class Dependency(Requirement):
    def __init__(
        self,
        pkg: str,
        *,
        conda_name: str = "",
        version: str = "",
        platform: str = "",
        python_version: str = "",
        markers: str = "",
        tag: str = "required",
    ):
        pkg_parse = pkg
        self._tag = tag

        python_version = python_version.replace("'", "").replace('"', "")
        py_match = re.match(r"\s*([!=><~^]+)\s*(.*)\s*", python_version, re.DOTALL)
        if py_match:
            python_version = f"{py_match.group(1)} '{py_match.group(2)}'"

        if version:
            try:
                version = SpecifierSet(version)
            except InvalidSpecifier:
                version = SpecifierSet(f"=={version}")
            pkg_parse += f" {version}"

        platform = self._get_platform_marker(platform)
        python_version = self._get_python_version_marker(python_version)

        if platform and python_version:
            markers_init = f"{platform} and ({python_version})"
        else:
            markers_init = f"{platform or python_version}"

        if markers_init and markers:
            pkg_parse += f"; ({markers}) and {markers_init}"
        elif markers_init or markers:
            pkg_parse += f"; {markers or markers_init}"

        super().__init__(pkg_parse)
        self.conda_name = conda_name.strip() or self.name

    @property
    def tag(self) -> str:
        return self._tag

    def _get_python_version_marker(self, python_version: str):
        if not python_version:
            return ""
        python_version = python_version.strip()
        if python_version[0].isnumeric():
            python_version = f"== '{python_version}'"
        return f"python_version {python_version}"

    def _get_platform_marker(self, platform: list[str] | str) -> str:
        if not platform:
            return ""
        if isinstance(platform, str):
            platform = [platform]
        platform_parsed = [f"os_name == '{p}'" for p in platform]
        platform_parsed = " or ".join(platform_parsed)
        return f"({platform_parsed})" if len(platform) > 1 else platform_parsed

    @property
    def conda_name(self) -> str:
        return self._conda_name

    @conda_name.setter
    def conda_name(self, conda_name: str):
        self._conda_name = re.sub(r"(\[.+\])", "", conda_name, re.DOTALL).strip()

    def __repr__(self) -> str:
        conda_name = ""
        if self.conda_name != self.name:
            conda_name = f"({self.conda_name})"
        return f"<Dependency[{self.tag}] {conda_name} {self}>"

    def __eq__(self, other: "Dependency"):
        return (
            super().__eq__(other)
            and other.conda_name == self.conda_name
            and other.tag == self.tag
        )

    def __hash__(self):
        return hash((super().__hash__(), self.conda_name, self.tag))

    @property
    def conda_dep_style(self):
        conda_pkg = self.conda_name
        if self.marker:
            conda_pkg += f"  # [{self._get_markers_in_conda_style()}]"
        return conda_pkg

    def _get_markers_in_conda_style(self, list_markers: list | None = None):
        list_markers = list_markers or self.marker._markers
        result = []
        for mk in list_markers:
            if isinstance(mk, tuple):
                if mk[0].value == "os_name":
                    if mk[1].value == "==":
                        result.append(mk[2].value)
                    elif mk[1].value == "!=":
                        result.append(f"(not {mk[2].value})")
                elif mk[0].value == "python_version":
                    py_version = re.sub(r"[\.\'\"]+", "", mk[2].value)
                    result.append(f"(py{mk[1].value}{py_version})")
                else:
                    result.append(mk)
            elif isinstance(mk, str):
                result.append(mk)
            elif isinstance(mk, list):
                result.append(f"({self._get_markers_in_conda_style(mk)})")
        return " ".join(result)
