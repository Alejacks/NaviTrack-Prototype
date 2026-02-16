import tomllib

from pathlib import Path
from typing import Any, Collection


def read_toml_file(file_path: str | Path) -> dict:
    if isinstance(file_path, str):
        file_path = Path(file_path)
    with open(file_path, "rb") as file:
        return tomllib.load(file)


def check_value_within_collection(needle: Any, haystack: Collection[Any]) -> bool:
    return needle in haystack


__all__ = ["read_toml_file", "check_value_within_collection"]