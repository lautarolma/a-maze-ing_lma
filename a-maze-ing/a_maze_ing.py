#!/usr/bin/env python3
import sys
from controller import setup_config, build_maze, run_visuals
from config import MazeConfigError
from ui import DisplayMazeError


def main():
    """Main function to run the maze generation and visualization."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return

    try:
        config = setup_config(sys.argv[1])   
        maze, pattern = build_maze(config)
        run_visuals(maze, pattern, config)

    except MazeConfigError as e:
        print(f"Configuration/Validation Error: {e}")
    except DisplayMazeError as e:
        print(f"UI Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nUser interrupted. Bye!")
        raise SystemExit(0)
