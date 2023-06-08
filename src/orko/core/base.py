from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet, InvalidSpecifier


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
    ):
        pkg_parse = pkg
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
        self._conda_name = conda_name.strip() or self.name

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
        result = "(" if len(platform) > 1 else ""
        for p in platform:
            if result:
                result += " or "
            result += f"os_name == '{p}'"
        result += ")" if len(platform) > 1 else ""
        return result

    @property
    def conda_name(self) -> str:
        return self._conda_name

    @conda_name.setter
    def _setter_conda_name(self, conda_name: str):
        self._conda_name = conda_name.strip()

