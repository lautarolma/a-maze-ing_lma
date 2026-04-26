#!/usr/bin/env python3
from .parser import MazeConfigError, ImposibleMazeError, ALLOWED_KEYS

def maze_validator(config: dict) -> bool:
    """
    """
    # required_keys = set(ALLOWED_KEYS)
    # if not required_keys.issubset(config.keys()):
    #     missing = required_keys - config.keys()
    #     raise MazeConfigError(f"Missing keys: {', '.join(missing)}")

    width = config["width"]
    height = config["height"]
    entry = config["entry"]
    exit = config["exit"]

    if width > 50:
        raise MazeConfigError(f"Width '{width}' exceeds the maximum "
                              "allowed value of 50.")
    if height > 50:
        raise MazeConfigError(f"Height '{height}' exceeds the maximum "
                              "allowed value of 50.")
    if not (entry[0] >= 0 and entry[0] < width and entry[1] >= 0
            and entry[1] < height):
        raise MazeConfigError(f"Entry coordinates {entry} are out of bounds "
                              f"for maze size {width}x{height}.")
    if not (exit[0] >= 0 and exit[0] < width and exit[1] >= 0
            and exit[1] < height):
        raise MazeConfigError(f"Exit coordinates {exit} are out of bounds "
                              f"for maze size {width}x{height}.")
    
    # Check for optional keys
    if config["seed"] is not None and not isinstance(config["seed"], int):
        raise MazeConfigError("Seed must be an integer if provided.")
    return True


def check_42_pattern(config: dict) -> bool:
    """
    """
    from mazegen import block_42_pattern
    width = config["width"]
    height = config["height"]
    entry = config["entry"]
    exit = config["exit"]
    patttern_42 = True
    if width < 15 or height < 15:
        print("Warning: Maze dimensions are too small to accommodate "
              "the '42' pattern. The pattern will be ignored.")
        patttern_42 = False
    if patttern_42:
        cells_to_block = block_42_pattern(width, height)
        if tuple(entry) in cells_to_block:
            raise ImposibleMazeError("Entry point is blocked by the 42 pattern.")
        if tuple(exit) in cells_to_block:
            raise ImposibleMazeError("Exit point is blocked by the 42 pattern.")

    return patttern_42
