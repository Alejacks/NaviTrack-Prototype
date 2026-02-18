import tomllib

from pathlib import Path
from typing import Any, Collection

__all__ = ["read_toml_file", "needle_on_haystack", "needle_on_barn"]


def read_toml_file(file_path: str | Path) -> dict:
    if isinstance(file_path, str):
        file_path = Path(file_path)
    with open(file_path, "rb") as file:
        return tomllib.load(file)


def needle_on_haystack(needle: Any, haystack: Collection[Any]) -> bool:
    return needle in haystack


def needle_on_barn(needle: Any, haystack: Any, barn: dict[Any, Any]) -> bool:
    if haystack in barn:
        return needle in barn[haystack]
    return False


def create_path_if_not_exists(path: Path) -> bool:
    try:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
        return True
    except PermissionError:
        return False
