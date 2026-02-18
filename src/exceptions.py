class TomlException(Exception):
    pass

class ConfigException(Exception):
    pass

class ConfigNotFoundException(ConfigException):
    pass