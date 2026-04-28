#!/usr/bin/python3

from config import parse_config, maze_validator, check_42_pattern
from ui import display, animation, determine_display_mode
from mazegen import Maze


def setup_config(file_path: str) -> dict:
    """initialize the configuration by parsing and validating the config file."""
    config = parse_config(file_path)
    maze_validator(config)
    return config

#### revisar esta funcion lo qe devuelve no tiene logica
def build_maze(config):
    """Generates the maze and applies the '42' pattern if applicable."""
    maze = Maze(config)
    maze.generate()

    pattern = None
    if check_42_pattern(config):
        pattern = maze.block_42_pattern(maze.width, maze.height)

    return maze, pattern


def run_visuals(maze, pattern, config):
    """Handles the display of the maze and the solution animation if enabled."""
    
    sol_path = maze.solve()

    # si no cabe imprime con solucion
    maze_fits = determine_display_mode(maze.width, maze.height)

    display(
        maze, 
        pattern, 
        sol_path, 
        maze_fits,
        #config["instant_solution"], 
        config["theme_idx"], 
        config["random_color"]
    )
    
    # si cabe imprime primero maze y luego solucion animada
    if maze_fits:
        animation(maze, sol_path, config["theme_idx"])

    maze.save_to_file()