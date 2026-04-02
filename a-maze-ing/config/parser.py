#!/usr/bin/python3
from typing import TypedDict, Tuple, Set, Optional
import os

# sets of the autorized keys
MANDATORY_KEYS: Set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    }

OPTIONAL_KEYS: Set[str] = {
        "SEED"
    }

ALLOWED_KEYS: Set[str] = MANDATORY_KEYS | OPTIONAL_KEYS

class MazeConfigError(Exception):
    """"""
    pass

class ConfigFormat(TypedDict):
    """Define dictionary that follows the format"""
    width: int
    height: int
    entry_xy: Tuple[int, int]
    exit_xy: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int]

def parse_coord(value: str) -> Tuple[int, int]:
    """Convert exit/entry coordinates into tuples"""
    coor = value.split(',')
    if len(coor) != 2:
        raise ValueError("Invalid format for entry/exit "
                         "(Expected x,y)")
    return (int(coor[0]), int(coor[1]))
            

def parse_config(config_file_path: str) -> ConfigFormat:
    """
    Parse the maze configuration file.

    Raise:
        MazeConfigError if key or value are invalid
        ValueError if value is not integrer
        FileNotFoundError if config file doesn't exist
    """
    # check if the file does exist
    if not os.path.exists(config_file_path):
        raise FileNotFoundError("Config file not found: "
                                f"{config_file_path}")
    else:
        # temporal dictionary to save the data and check
        temp: dict[str, str] = {}
        try:
            with open(config_file_path) as file:
                content = file.readlines()
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
            if "SEED" not in temp or not temp["SEED"]:
                seed = None
            else:
                try:
                    seed = int(temp["SEED"])
                except ValueError:
                    raise MazeConfigError(f"'SEED' value '{temp['SEED']}' "
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
            entry_xy = parse_coord(temp["ENTRY"])
            exit_xy = parse_coord(temp["EXIT"])
            # PERFECT MAZE
            perfect_str = temp["PERFECT"].lower()
            if perfect_str not in ("true", "false"):
                raise ValueError("PERFECT needs to be 'true' or 'false'.")
            if perfect_str == "true":
                perfect = True
            else:
                perfect = False
            # Return ConfigFormat
            return {
                    "width": width,
                    "height": height,
                    "entry": entry_xy,
                    "exit": exit_xy,
                    "output_file": temp["OUTPUT_FILE"],
                    "perfect": perfect,
                    "seed": seed
                    }
        except (ValueError, MazeConfigError) as e:
            print(f"Configuration failed: {e}")
        
diccionario = parse_config("config.txt")
print("aqui está el diccionario: ", diccionario)