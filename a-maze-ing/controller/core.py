import sys
from config import ConfigFormat, parse_config, maze_validator, check_42_pattern
from ui import (
    animation,
    header_animation,
    static_header,
    menu_visuals,
    display_maze,
    DisplayMazeError
)
from mazegen import MazeGenerator as Maze
try:
    import readchar
except ImportError:
    print("[ERROR] Library 'readchar' is missing", file=sys.stderr)
    print("please run 'make install' (or: 'pip install .') "
          "to install the required dependencies", file=sys.stderr)
    sys.exit(1)


def setup_config(file_path: str) -> ConfigFormat:
    """initialize the configuration by parsing and validating the config file.
    Args:    file_path (str): The path to the configuration file.
    Returns:    ConfigFormat: The validated configuration dictionary."""

    config = parse_config(file_path)
    maze_validator(config)

    return config


def build_maze(config) -> tuple[Maze, list[tuple[int, int]] | None]:
    """Generates the maze and applies the '42' pattern if applicable.
    returns the maze object and the pattern cells if the pattern is applied.
    Args:
        config (dict):
            The configuration dictionary containing
            settings for the maze generation.
    Returns:
        tuple[Maze, list[tuple[int, int]] | None]:
            A tuple containing the generated maze object and a list of
            coordinates for the '42' pattern cells, or None if the pattern
            is not applied."""

    maze = Maze(
        width=config["width"],
        height=config["height"],
        entry_xy=config["entry_xy"],
        exit_xy=config["exit_xy"],
        perfect=config["perfect"],
        seed=config["seed"]
    )
    maze.generate()
    pattern = None
    if check_42_pattern(config):
        pattern = maze.block_42_pattern(maze.width, maze.height)

    return maze, pattern


def run_visuals(maze, pattern, config) -> None:
    """Handles the display of the maze and the user interaction loop
    for regenerating the maze, toggling the solution animation,
    changing color themes, and quitting the program.
     Args:
        maze (Maze):
            The maze object to be displayed.
        pattern (list[tuple[int, int]] | None):
            List of coordinates for the '42'
            pattern cells, or None if the pattern is not applied.
        config (dict):
            The configuration dictionary containing settings for the maze
            generation and display.
    raises:
        DisplayMazeError:
            If there is an error during the display
            of the maze or the solution animation."""

    print("\033[H\033[J\033[3J", end="")
    running = True
    show_solution = False
    header_animation()

    while running:

        print("\033[H\033[2J\033[3J", end="", flush=True)

        static_header()

        try:
            display_maze(
                maze,
                pattern,
                maze.solve(),
                config["theme_idx"],
                config["random_color"]
            )

        except DisplayMazeError as e:
            print(f"\nDisplayMazeError: {e}")
            return

        if show_solution:

            try:
                animation(maze, maze.solve(), config["theme_idx"])

            except DisplayMazeError as e:
                print(f"\n\nDisplayMazeError: {e}")
                print("bye!")
                return

        menu_visuals(config["theme_idx"])

        try:

            key = readchar.readkey()

            if key == "q" or key == "Q":
                running = False

            elif key == "r" or key == "R":
                show_solution = False
                maze, pattern = build_maze(config)

            elif key == "s" or key == "S":
                show_solution = not show_solution

            elif key == "c" or key == "C":
                config["theme_idx"] = (config["theme_idx"] + 1) % 5

            else:
                print("\a", end="")

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Bye!...", file=sys.stderr)
            return

        maze.save_to_file(config["output_file"])

    print("\033[H\033[J\033[3J", end="")
    print("bye!")
