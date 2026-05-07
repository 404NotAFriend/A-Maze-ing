import sys
from typing import Any


class ConfigError(Exception):
    """
    Custom exception for config
    """
    pass


def get_config_path() -> str:
    """
    Get the config file_name
    If no configuration is given as an argument,
    Use the default_config.txt as default
    """
    if len(sys.argv) > 1:
        return sys.argv[1]
    raise ValueError("No .txt file provided.")


def check_mandatory_keys(config_keys: dict[str, Any]) -> None:
    """
    Check if all the mandatory keys are present and uncommented
    From the config file
    If not: raise an error - The maze can't be generated
    """
    required_k = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    missing = required_k - config_keys.keys()

    if missing:
        raise ConfigError(
            f"Missing required key(s): {', '.join(missing)}"
        )


def parse_config(file_path: str) -> dict[str, Any]:
    """
    Read and transform the values of config.txt into a dict
    """
    config: dict[str, Any] = {}

    try:
        with open(file_path, "r") as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()

                # Ignore empty lines and comments
                if not line or line.startswith('#'):
                    continue

                if "=" not in line:
                    raise ConfigError(f"Invalid format on line {i}.")

                key, value = line.split("=", 1)  # maxsplit=1
                key = key.strip()  # Remove extra spaces
                value = value.strip()

                if key in config:
                    raise ConfigError(f"Duplicate key '{key}' on line {i}.")

                config[key] = value
        check_mandatory_keys(config)
        return config

    except FileNotFoundError:
        raise ConfigError(f"File '{file_path}' was not found.")


def convert_config(config: dict[str, Any]) -> dict[str, Any]:
    """
    Converts config values to proper types (int, tuple, bool)
    """
    for key, value in config.items():
        if key in ("WIDTH", "HEIGHT", "SEED"):
            try:
                config[key] = int(value)
            except ValueError:
                raise ConfigError(f"{key} must be an integer")

        elif key in ("ENTRY", "EXIT"):
            try:
                x_str, y_str = value.split(",")
                x = int(x_str.strip())
                y = int(y_str.strip())
                config[key] = (x, y)
            except ValueError:
                raise ConfigError(f"{key} must be in format x,y")

        elif key == "PERFECT":
            val = value.lower()
            if val == "true":
                config[key] = True
            elif val == "false":
                config[key] = False
            else:
                raise ConfigError("PERFECT must be True or False")
    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit_ = config["EXIT"]

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive")

    if entry == exit_:
        raise ConfigError("ENTRY and EXIT must have different values")

    for name, (x, y) in (("ENTRY", entry), ("EXIT", exit_)):
        if not (0 <= x < width and 0 <= y < height):
            raise ConfigError(f"{name} must be inside maze bounds")
    return config
