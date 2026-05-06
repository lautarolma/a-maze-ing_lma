#!/usr/bin/python3

import os
import time
import readchar
from config import parse_config, maze_validator, check_42_pattern
from ui import animation, determine_display_mode, header_yield, menu_visuals
from mazegen import Maze
from ui.display import display_maze



def setup_config(file_path: str) -> dict:
    """initialize the configuration by parsing and validating the config file."""
    config = parse_config(file_path)
    maze_validator(config)
    return config

#### revisar esta funcion lo qe devuelve no tiene logica // devuelve tupla, objeto maze + coor del patron 42
def build_maze(config) -> tuple[Maze, list[tuple[int, int]] | None]:
    """Generates the maze and applies the '42' pattern if applicable.
    returns the maze object and the pattern cells if the pattern is applied."""
    maze = Maze(config)
    maze.generate()

    pattern = None
    if check_42_pattern(config):
        pattern = maze.block_42_pattern(maze.width, maze.height)

    return maze, pattern


def run_visuals(maze, pattern, config):
    """Handles the display of the maze and the solution animation if enabled."""

    running = True

    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "header.txt")

        for c in header_yield(file_path):
            print(c, end="", flush=True)
            time.sleep(0.00005)
            print("\033[s", end="")

    except FileNotFoundError as e:
        print(f"Caught an error: {e}")

    MARGIN = 20
    show_solution = False

    while running:
        print(f"\033[{MARGIN};1H", end="")
        print("\033[J", end="")

        # si no cabe imprime con solucion
        #maze_fits = determine_display_mode(maze.width, maze.height)
        try:
            display_maze(
                maze, 
                pattern, 
                maze.solve(),
                #maze_fits,
                config["theme_idx"], 
                config["random_color"]
            )
        except Exception as e:
            print(f"Error displaying maze: {e}")
            running = False
            

        # si cabe imprime primero maze y luego solucion animada
        if show_solution:
            animation(maze, maze.solve(), config["theme_idx"])

        menu_visuals()

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

        maze.save_to_file()
    
    print("\033[H\033[J\033[3J", end="")
    print("bye!")
