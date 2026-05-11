#!/usr/bin/env python3
import sys
from .parser import ConfigFormat, MazeConfigError, ImposibleMazeError


def maze_validator(config: ConfigFormat) -> bool:
    """
    Validate the maze configuration dictionary against
    defined rules and constraints.

    Args:
        config (ConfigFormat): A dictionary containing maze parameters such as
            width, height, entry_xy, exit_xy, and seed.

    Returns:
        bool: True if the configuration is valid.

    Raises:
        MazeConfigError: If the dimensions exceed 60, coordinates
            are out of bounds, or the seed is not an integer.
        ImposibleMazeError: If the width or height is below
            the minimum value of 5.
    """
    width = config["width"]
    height = config["height"]
    entry = config["entry_xy"]
    exit = config["exit_xy"]

    if width > 60 or height > 60:
        raise MazeConfigError(f"Width '{width if width > 50 else height}' "
                              "exceeds the maximum allowed value of 50.")
    if width < 5 or height < 5:
        raise ImposibleMazeError(f"Width '{width if width < 5 else height}' "
                                 "is below the minimum allowed value of 5.")
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


def check_42_pattern(config: ConfigFormat) -> bool:
    """
    Check if the '42' pattern can be applied to the maze configuration.

    Args:
        config (ConfigFormat): A dictionary containing maze parameters,
            including width, height, entry_xy, and exit_xy.

    Returns:
        bool: True if the pattern is applicable,
        False if the maze is too small.

    Raises:
        ImposibleMazeError: If the entry or exit point is located within
            the coordinates blocked by the '42' pattern.
    """
    from mazegen import block_42_pattern
    width = config["width"]
    height = config["height"]
    entry = config["entry_xy"]
    exit = config["exit_xy"]
    use_patttern_42 = True
    if width < 15 or height < 15:
        print("Warning: Maze dimensions are too small to accommodate "
<<<<<<< HEAD
              "the '42' pattern. The pattern will be ignored.")
        use_patttern_42 = False
    if use_patttern_42:
=======
              "the '42' pattern. The pattern will be ignored.",
              file=sys.stderr)
        patttern_42 = False
    if patttern_42:
>>>>>>> imperfect_maze
        cells_to_block = block_42_pattern(width, height)
        if tuple(entry) in cells_to_block:
            raise ImposibleMazeError(
                "Entry point is blocked by the 42 pattern."
                )
        if tuple(exit) in cells_to_block:
            raise ImposibleMazeError(
                "Exit point is blocked by the 42 pattern."
                )

    return use_patttern_42
