'''
What do we need to do? Read configurations from the configuration path constant (which is a TOML), parse it, and be able to access the configuration values from a class instance (which

For config.py:

- Singleton class with a configuration dictionary - config.py / It was decided that a module would be better than a singleton / Done
- Constant with the path of the configuration file - config.py / Done
- Methods to read the configuration values and parse them from a TOML into a dictionary - utils.py / Done
- Methods to check if the configuration values are valid (and exceptions for errors in this case)- utils.py
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
from typing import Any

from src import utils

CONFIG_FILE_PATH: Path = Path(__file__).parent.parent / "config.toml"

VALID_EXPIRATION_TIME_UNITS: tuple[str, ...] = ("ms", "s", "m", "h", "d")

VALID_EXPIRATION_BEHAVIOR: tuple[str, ...] = ("shadow", "delete", "backup")

VALID_ON_DUPLICATE_BEHAVIOR: tuple[str, ...] = ("overwrite", "rename", "error")


class Config:
    __config__: dict[str, Any]

    def __init__(self, config_file_path: Path = CONFIG_FILE_PATH):
        self.__config__ = utils.read_toml_file(config_file_path)



    def values(self) -> dict[str, Any]:
        return self.__config__
