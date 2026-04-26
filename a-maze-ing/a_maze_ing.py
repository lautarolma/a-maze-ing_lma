#!/usr/bin/env python3
import sys
from config import parse_config, maze_validator, MazeConfigError, check_42_pattern
from ui import display, DisplayMazeError
from mazegen import Maze

def a_maze_ing() -> None:
    """
    """
    config = None
    if len(sys.argv) == 2:
        try:
            file = sys.argv[1]
            config = parse_config(file)
        except MazeConfigError as e:
            print(f"Configuration failed: {e}")
            return
        
        if config:
            try:
                maze_validator(config)
                a_maze_ing = Maze(config)
                a_maze_ing._generate_maze()
                if check_42_pattern(config):
                    pattern = a_maze_ing.block_42_pattern(config["width"],
                                                          config["height"])
                else:
                    pattern = None
            except MazeConfigError as e:
                print(f"Validation failed: {e}")
                return

        try:
            display(a_maze_ing, pattern)
            a_maze_ing.save_to_file()
        except DisplayMazeError as e:
            print(f"DisplayError occurred: {e}")
    else:
        print("No arguments recieved")


a_maze_ing()
