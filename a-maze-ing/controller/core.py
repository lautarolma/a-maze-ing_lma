#!/usr/bin/python3

from config import parse_config, maze_validator, check_42_pattern
from ui import display, animate_solution
from mazegen import Maze


def setup_config(file_path: str):
    """initialize the configuration by parsing and validating the config file."""
    config = parse_config(file_path)
    maze_validator(config)
    return config


def build_maze(config):
    """Generates the maze and applies the '42' pattern if applicable."""
    maze = Maze(config)
    maze.generate()

    pattern = None
    if check_42_pattern(config):
        pattern = maze.block_42_pattern(maze.width, maze.height)

    return maze, pattern


def run_visuals(maze, pattern, config):
    """"Handles the display of the maze and the solution animation if enabled.""""
    sol_path = maze.solve() if config["instant_solution"] else None

    display(
        maze, pattern, sol_path, 
        config["instant_solution"], 
        config["theme_idx"], 
        config["random_color"]
    )

    if sol_path and config["instant_solution"]:
        animate_solution(maze, sol_path, config["theme_idx"])

    maze.save_to_file()