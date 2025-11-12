from importlib.resources import files
from pathlib import Path
from typing import cast


def rootPath() -> Path:
    return cast(Path, files("mpl_theme_tweaker"))


def resourcePath() -> Path:
    return rootPath() / "resources"


def logPath() -> Path:
    return rootPath() / "../.."


if __name__ == "__main__":
    print("rootPath:", rootPath())
    print("resourcePath:", resourcePath())
