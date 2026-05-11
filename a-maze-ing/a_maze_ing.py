#!/usr/bin/env python3
import bdb
import sys
from controller import setup_config, build_maze, run_visuals
from config import MazeConfigError
from ui import DisplayMazeError


def main() -> None:
    """Main function to run the maze generation and visualization."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        return

    try:
        config = setup_config(sys.argv[1])
        print("tenemos config:", config)
        maze, pattern = build_maze(config)
        print("hemos creado el maze y el pattern:")
        run_visuals(maze, pattern, config)

    except MazeConfigError as e:
        print(f"Configuration/Validation Error: {e}", file=sys.stderr)
    except DisplayMazeError as e:
        print(f"DisplayMazeError Error: {e}", file=sys.stderr)
    except Exception as e:
    #    print(f"Unexpected Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except bdb.BdbQuit:
        print("Debugger session ended.", file=sys.stderr)
        raise SystemExit(0)
    except (KeyboardInterrupt, EOFError):
        print("\nUser interrupted. Bye!", file=sys.stderr)
        raise SystemExit(0)
