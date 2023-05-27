from setuptools.build_meta import build_sdist as setuptools_build_sdist
from setuptools.build_meta import build_wheel as setuptools_build_wheel

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    return setuptools_build_wheel(
        wheel_directory,
        config_settings=config_settings,
        metadata_directory=metadata_directory,
    )


def build_sdist(sdist_directory, config_settings=None):
    return setuptools_build_sdist(sdist_directory, config_settings)