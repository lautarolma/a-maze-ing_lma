import readchar
from config import parse_config, maze_validator, check_42_pattern
from ui import animation, header_animation, menu_visuals, display_maze, DisplayMazeError
from mazegen import Maze


def setup_config(file_path: str) -> dict:
    """initialize the configuration by parsing and validating the config file.
    Args:    file_path (str): The path to the configuration file.
    Returns:    dict: The validated configuration dictionary."""

    config = parse_config(file_path)
    maze_validator(config)

    return config


def build_maze(config) -> tuple[Maze, list[tuple[int, int]] | None]:
    """Generates the maze and applies the '42' pattern if applicable.
    returns the maze object and the pattern cells if the pattern is applied.
    Args:
        config (dict): The configuration dictionary containing settings for the maze generation.
    Returns:
        tuple[Maze, list[tuple[int, int]] | None]: A tuple containing the generated maze object
        and a list of coordinates for the '42' pattern cells, or None if the pattern is not applied."""
    
    maze = Maze(config)
    maze.generate()
    pattern = None
    if check_42_pattern(config):
        pattern = maze.block_42_pattern(maze.width, maze.height)

    return maze, pattern


def run_visuals(maze, pattern, config) -> None:
    """Handles the display of the maze and the user interaction loop for regenerating the maze,
    toggling the solution animation, changing color themes, and quitting the program.
     Args:
        maze (Maze): The maze object to be displayed.
        pattern (list[tuple[int, int]] | None): List of coordinates for the '42'
            pattern cells, or None if the pattern is not applied.
        config (dict): The configuration dictionary containing settings for the maze
            generation and display.
    raises:        DisplayMazeError: If there is an error during the display of the maze or the solution animation."""

    running = True
    show_solution = False
    MARGIN = 20

    header_animation()
 
    while running:
        print(f"\033[{MARGIN};1H", end="")
        print("\033[J", end="")
        # si no cabe imprime con solucion
        try:
            display_maze(
                maze, 
                pattern, 
                maze.solve(),
                #maze_fits,
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

        key = readchar.readkey()

        if key == "q":
            running = False

        elif key == "r":
            show_solution = False
            maze, pattern = build_maze(config)

        elif key == "s":
            show_solution = not show_solution

        elif key == "c":
            config["theme_idx"] = (config["theme_idx"] + 1) % 5

        else:
            print("\a", end="")

        maze.save_to_file()
    
    print("\033[H\033[J\033[3J", end="")
    print("bye!")
