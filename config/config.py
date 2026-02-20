'''
What do we need to do? Read configurations from the configuration path constant (which is a TOML), parse it, and be able to access the configuration values from a class instance.

For config.py:

- Singleton class with a configuration dictionary - config.py / It was decided that a module would be better than a singleton / Done
- Constant with the path of the configuration file - config.py / Done
- Methods to read the configuration values and parse them from a TOML into a dictionary - utils.py / Done
- Constants for valid values so validating the TOML file is easier - config.py / Done
- Methods to check if the configuration values are valid (and exceptions for errors in this case) - config.py
- Method to validate the configuration values and raise an exception if they are invalid - config.py
- Method to validate the TOML has no duplicated values within the same layer - utils.py
- Method to get the number of layers in each dictionary - utils.py
- Method to access the configuration values from the dictionary - config.py
- Method to access the configuration values from a dictionary inside a dictionary (and so on) - config.py based on utils.py methods to get values from a dictionary inside a dictionary...

- Custom exceptions for different errors - exceptions.py

Crazy idea: What about a class for a layer? Maybe we can have a class for each layer, and each layer has a method to access the configuration values from the dictionary, which can make the code more readable.
Each layer instance would also specify the layer number level

We're keeping that for a later version.

Methods should be distributed within utils.py and config.py, config.py should only contain the configuration dictionary and the methods to read and validate it.\

//

On the other hand, when it comes to DB and so on, DB should exist, have different tables (aliases, and yet to decide if other tables are needed), and have methods to access them.
All this should be checked and validated before proceeding on the program execution.
'''
from pathlib import Path
from typing import Any, Literal

from src import utils
from src.exceptions import ConfigException, ConfigNotFoundException

CONFIG_FILE_PATH: Path = Path(__file__).parent.parent / "config.toml"

DB_SECTION = "db"
NAVITRACK_SECTION = "navitrack"
EXPIRATION_SECTION = "expiration"

DB_FILE_KEY = "db_file"
ON_COLLIDE_KEY = "on_collide"

EXPIRATION_TIME_KEY = "time"
EXPIRATION_UNIT_KEY = "unit"
EXPIRATION_BEHAVIOR_KEY = "behavior"

FRECENCY_KEY = "frecency"

ExpirationUnit = Literal["ms", "s", "m", "h", "d"]
ExpirationBehavior = Literal["shadow", "delete", "backup"]
OnCollideBehavior = Literal["overwrite", "rename", "error"]

VALID_EXPIRATION_TIME_UNITS: tuple[ExpirationUnit, ...] = ("ms", "s", "m", "h", "d")
VALID_EXPIRATION_BEHAVIOR: tuple[ExpirationBehavior, ...] = ("shadow", "delete", "backup")
VALID_ON_COLLIDE_BEHAVIOR: tuple[OnCollideBehavior, ...] = ("overwrite", "rename", "error")

DEFAULT_EXPIRATION_TIME_UNIT: ExpirationUnit = "m"
DEFAULT_EXPIRATION_BEHAVIOR: ExpirationBehavior = "shadow"
DEFAULT_ON_COLLIDE_BEHAVIOR: OnCollideBehavior = "overwrite"
DEFAULT_FRECENCY_VALUE: bool = True

UNIT_TO_MS: dict[ExpirationUnit, int] = {
    "ms": 1,
    "s": 1_000,
    "m": 60_000,
    "h": 3_600_000,
    "d": 86_400_000,
}


def ensure_db_file_exists(db_file_path: Path) -> None:
    created: bool = utils.create_path_if_not_exists(db_file_path)
    if not created:
        raise ConfigException(
            f"Failed to create DB file path: '{db_file_path}' due to permission denied."
        )


class Config:
    _config: dict[str, Any]

    expiration_unit: ExpirationUnit | None
    expiration_time: int | None
    expiration_behavior: ExpirationBehavior | None
    expiration_time_in_milliseconds: int | None

    db_file_path: Path
    on_collide: OnCollideBehavior
    frecency: bool

    def __init__(self, config_file_path: Path = CONFIG_FILE_PATH) -> None:
        self._config = utils.read_toml_file(config_file_path)
        self._check_configuration_values()
        self._set_expiration_time_in_milliseconds()

    def values(self) -> dict[str, Any]:
        return dict(self._config)

    def _check_configuration_values(self) -> None:
        self._check_db_values()
        self._check_navitrack_values()
        self._check_expiration_values()

    def _require_section(self, section: str) -> dict[str, Any]:
        if section in self._config:
            return self._config[section]
        raise ConfigNotFoundException(
            f"{section} configuration not found. Please check your configuration file on {CONFIG_FILE_PATH}."
        )

    def _optional_section(self, section: str) -> dict[str, Any] | None:
        return self._config.get(section)

    def _check_db_values(self) -> None:
        db_values = self._require_section(DB_SECTION)

        if DB_FILE_KEY not in db_values:
            raise ConfigNotFoundException(
                f"{DB_FILE_KEY} not found in {DB_SECTION} configuration."
            )

        db_path = Path(db_values[DB_FILE_KEY])
        ensure_db_file_exists(db_path)
        self.db_file_path = db_path

        on_collide = db_values.get(ON_COLLIDE_KEY, DEFAULT_ON_COLLIDE_BEHAVIOR)
        if on_collide not in VALID_ON_COLLIDE_BEHAVIOR:
            raise ConfigException(f"Invalid on_collide behavior: {on_collide}")

        self.on_collide = on_collide

    def _check_navitrack_values(self) -> None:
        navitrack_values = self._optional_section(NAVITRACK_SECTION)

        if navitrack_values is None:
            self.frecency = DEFAULT_FRECENCY_VALUE
            return

        frecency = navitrack_values.get(FRECENCY_KEY, DEFAULT_FRECENCY_VALUE)
        if not isinstance(frecency, bool):
            raise ConfigException(
                f"Frecency must be a boolean: {frecency}. Got {type(frecency)} instead."
            )

        self.frecency = frecency

    def _check_expiration_values(self) -> None:
        expiration_values = self._optional_section(EXPIRATION_SECTION)

        if expiration_values is None:
            self.expiration_time = None
            self.expiration_unit = None
            self.expiration_behavior = None
            return

        expiration_time = expiration_values.get(EXPIRATION_TIME_KEY)

        if expiration_time is None:
            self.expiration_time = None
            self.expiration_unit = None
            self.expiration_behavior = None
            return

        if not isinstance(expiration_time, int):
            raise ConfigException(
                f"Expiration time must be an integer: {expiration_time}. Got {type(expiration_time)} instead."
            )

        if expiration_time < 0:
            raise ConfigException(f"Invalid expiration time: {expiration_time}. Expected a non-negative integer.")

        expiration_unit = expiration_values.get(
            EXPIRATION_UNIT_KEY, DEFAULT_EXPIRATION_TIME_UNIT
        )
        if expiration_unit not in VALID_EXPIRATION_TIME_UNITS:
            raise ConfigException(
                f"Invalid expiration time unit: {expiration_unit}. Valid units are: {', '.join(VALID_EXPIRATION_TIME_UNITS)}")

        expiration_behavior = expiration_values.get(
            EXPIRATION_BEHAVIOR_KEY, DEFAULT_EXPIRATION_BEHAVIOR
        )
        if expiration_behavior not in VALID_EXPIRATION_BEHAVIOR:
            raise ConfigException(
                f"Invalid expiration behavior: {expiration_behavior}. Valid behaviors are: {', '.join(VALID_EXPIRATION_BEHAVIOR)}"
            )

        self.expiration_time = expiration_time
        self.expiration_unit = expiration_unit
        self.expiration_behavior = expiration_behavior

    def _set_expiration_time_in_milliseconds(self) -> None:
        if self.expiration_time is None or self.expiration_unit is None:
            self.expiration_time_in_milliseconds = None
            return

        multiplier = UNIT_TO_MS[self.expiration_unit]
        self.expiration_time_in_milliseconds = self.expiration_time * multiplier