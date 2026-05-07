from typing import TypedDict, Dict

# sets of the autorized keys
MANDATORY_KEYS: set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
    }

OPTIONAL_KEYS: set[str] = {
        "SEED",
        "PERFECT",
        "RANDOM_COLOR",
        "INSTANT_SOLUTION",
        "SEED",
        "THEME_IDX"
    }

ALLOWED_KEYS: set[str] = MANDATORY_KEYS | OPTIONAL_KEYS


class MazeConfigError(Exception):
    """Exception raised for errors in the maze configuration."""
    pass


class ImposibleMazeError(MazeConfigError):
    """Exception raised when the maze configuration is impossible."""

    pass


class ConfigFormat(TypedDict):
    """Define dictionary that follows the format

    Raise:
        ValueError if the values are not in the expected format.
        MazeConfigError if the config file is not valid
    """
    width: int
    height: int
    entry_xy: tuple[int, int]
    exit_xy: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None
    seed: int | None
    theme_idx: int
    instant_solution: bool
    random_color: bool


def parse_coord(value: str) -> tuple[int, int]:
    """Convert exit/entry coordinates into tuples"""

    coor = value.split(',')
    if len(coor) != 2:
        raise ValueError("Invalid format for entry/exit "
                         "(Expected x,y)")
    try:
        x = int(coor[0])
        y = int(coor[1])
        return (x, y)
    except ValueError:
        raise MazeConfigError(f"Invalid coordinate value: '{value}' "
                              "(Expected x,y with integers)") from None


def parse_config(config_file_path: str) -> ConfigFormat:
    """
    Parse the maze configuration file.

    Raise:
        MazeConfigError if key or value are invalid
        ValueError if value is not integrer
        FileNotFoundError if config file doesn't exist
    """
    # temporal dictionary to save the data and check
    temp: Dict[str, str] = {}
    try:
        with open(config_file_path, mode="r", encoding="utf-8") as file:
            content = file.readlines()

    except FileNotFoundError as e:
        raise MazeConfigError("Config file not found: "
                              f"{config_file_path}: {e}")

    except PermissionError as e:
        raise MazeConfigError("Permission error trying to open: "
                              f"{config_file_path}: {e}")

    except IsADirectoryError as e:
        raise MazeConfigError(f"{config_file_path} is a directory: {e}")

    except OSError as e:
        raise MazeConfigError("OS error opening config file "
                              f"'{config_file_path}': {e}")

    # saves in a list of tuples, nb of line and content
    # line.strip() return "" if is an empty line
    data_lines = [(i, line.strip()) for i, line
                  in enumerate(content, start=1)
                  if line.strip() and not line.strip().startswith('#')]

    # format check
    for i, line in data_lines:
        if "=" not in line:
            raise MazeConfigError("Invalid format. Expected KEY=VALUE")

        key, value = line.split("=")
        key = key.upper()
        if not key:
            raise MazeConfigError(f"'KEY' is empty in line {i}")

        if key == "SEED" and not value:
            continue

        if key in temp:
            raise MazeConfigError(f"Duplicated key '{key}' in line {i}")

        temp[key] = value

    # allowed and missing keys check
    all_keys = temp.keys()
    not_allowed = [k for k in all_keys - ALLOWED_KEYS]
    missing_key = [k for k in MANDATORY_KEYS - all_keys]

    if not_allowed:
        raise MazeConfigError("Unknown key(s) in "
                              f"config file: {not_allowed}")

    if missing_key:
        raise MazeConfigError(f"Missing required key(s): {missing_key}")

    # parsing values
    # SEED
    raw_seed = temp.get("SEED")

    if raw_seed is None or raw_seed == "":
        seed = None
    else:
        try:
            seed = int(raw_seed)
        except ValueError:
            raise MazeConfigError(f"'SEED' value '{raw_seed}' "
                                  "is not a valid number")
    # WIDTH AND HEIGHT
    w = temp["WIDTH"]
    h = temp["HEIGHT"]
    width = int(w)
    height = int(h)
    if width <= 0 or height <= 0:
        raise MazeConfigError('WIDTH and HEIGHT must be positive '
                              'integers greater than 0. Entered '
                              f'W: {w} and H: {h}')
    # ENTRY AND EXIT
    try:
        entry_xy = parse_coord(temp["ENTRY"])
        exit_xy = parse_coord(temp["EXIT"])
    except ValueError as e:
        raise MazeConfigError(f"Invalid coordinate value: {e}")

    # PERFECT MAZE
    perfect_str = temp["PERFECT"].lower()
    if perfect_str not in ("true", "false"):
        raise ValueError("PERFECT needs to be 'true' or 'false'.")
    perfect = (perfect_str == "true")

    # UI SETTINGS (default values)
    theme_idx = int(temp.get("THEME_IDX", 4))
    random_color = temp.get("RANDOM_COLOR", "false").lower() == "true"

    # Return ConfigFormat
    return {
            "width": width,
            "height": height,
            "entry": entry_xy,
            "exit": exit_xy,
            "output_file": temp["OUTPUT_FILE"],
            "perfect": perfect,
            "seed": seed,
            "theme_idx": theme_idx,
            # "instant_solution": instant_solution,
            "random_color": random_color
            }


# dict = parse_config("config.txt")
# if __name__ == "__main__":
#     import sys
#     try:
#         dict = parse_config("config.txt")
#         print("Lectura manual exitosa, aqui está el diccionario: ", dict)
#     except Exception as e:
#         print("Test fallido con error:"
#               f"\n{type(e).__name__}: {e}", file=sys.stderr)
