from __future__ import annotations
import os
import random
from typing import Generator
import time
from mazegen import Maze
import shutil

# Estilos
COLOR_PALETTE = [
    # 0: bg,           1: path,          2: font,          3: p42,          4: ec
    # night
    ["\033[48;5;17m", "\033[48;5;229m", "\033[38;5;195m", "\033[48;5;51m", "\033[0m"],
    # uzumaki
    ["\033[48;5;208m", "\033[48;5;220m", "\033[38;5;238m", "\033[48;5;238m", "\033[0m"],
    # akatsuki
    ["\033[48;5;233m", "\033[48;5;251m", "\033[38;5;251m", "\033[48;5;124m", "\033[0m"],
    # dark mode
    ["\033[48;5;233m", "\033[48;5;236m", "\033[38;5;236m", "\033[48;5;220m", "\033[0m"],
    # eva01
    ["\033[48;5;128m", "\033[48;5;54m", "\033[38;5;54m", "\033[48;5;76m", "\033[0m"],
    # ox
    ["\033[48;5;55m", "\033[48;5;177m", "\033[38;5;177m", "\033[48;5;99m", "\033[0m"]
]


class DisplayMazeError(Exception):
    """Exception raised for errors in the maze display process."""
    pass


# print maze
def print_maze(
        maze: Maze,
        pattern_42: set[tuple[int, int]],
        solution_path: list[tuple[int, int]] | None = None,
        maze_fits: bool = False,
        theme_idx: int = 4,
        random_color: bool = False
        ) -> int:
    """
    Prints the maze to the terminal with optional
    styling and solution path.
     Args:
        maze (Maze): The maze object to be printed.
        pattern_42 (set[tuple[int, int]]):
        Set of coordinates for the 42 pattern.
        solution_path (list[tuple[int, int]], optional):
        List of coordinates for the solution path. Defaults to None.
        animated_solution (bool, optional):
        Whether to animate the solution path. Defaults to False.
        theme_idx (int, optional):
        Index for the color theme. Defaults to 4.
        random_color (bool, optional):
        Whether to select a random color theme. Defaults to False.
    """
    if random_color:
        theme_idx = random.randint(0, len(COLOR_PALETTE) - 1)

    bg = COLOR_PALETTE[theme_idx][0]
    ft = COLOR_PALETTE[theme_idx][3]
    font = COLOR_PALETTE[theme_idx][2]
    path = COLOR_PALETTE[theme_idx][1]
    ec = COLOR_PALETTE[theme_idx][4]

    r_style = bg + font

    sol_set: set[tuple[int, int]] = (
        set(solution_path) if solution_path else set[tuple[int, int]]()
    )

    top_line = r_style
    solved_path = [coord for coord, _ in sol_set]

    for x in range(maze.width):
        top_line += "+---"
    top_line += "+" + ec
    print(top_line)

    # 🔹 Por cada fila del maze
    for y in range(maze.height):

        # vertical cells
        line_cells = r_style + "|"

        # bottom line of cells
        line_bottom = r_style

        for x in range(maze.width):
            cell = maze.grid[x][y]

            # check if the cell is entry, exit, in 42 pattern or normal cell
            if (x, y) == maze.entry_xy or (x, y) == maze.exit_xy:
                content = path + " * " + ec + r_style
            elif (pattern_42 and (x, y) in pattern_42):
                content = ft + " * " + ec + r_style
            elif (x, y) in solved_path and not maze_fits:
                # render solution path
                content = path + " • " + ec + r_style
            else:
                content = "   "

            # East wall
            east_wall = "|" if cell.walls["E"] else " "

            # build line of cells
            line_cells += content + east_wall

            # South wall
            if cell.walls["S"]:
                line_bottom += "+---"
            else:
                line_bottom += "+   "

        # Close the line of cells
        line_cells += ec
        line_bottom += "+" + ec

        # Print the two lines
        print(line_cells)
        print(line_bottom)


def header_yield(file_path: str) -> Generator[dict, None, None]:
    """
    Reads a file and yields its content character by character with a delay.
    """
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            for c in line:
                yield c

# For print over terminal output, we must use print("\033[) with the specific flag:

# 's' saves a checkpoint of the current terminal-cursor position.
# 'u' return the cursor-position to the last checkpoint saved.
# {value} + 'A' moves the terminal-cursor to up direction n_value times.
# {value} + 'C' moves the terminal-cursor to right direction n_value times.

def animation(maze, solution_path: list, theme_idx: int = 4) -> None:
    """
    prints step by step the solution path with a delay between each step.
    """
    sol_color = COLOR_PALETTE[theme_idx][1] 
    ec = COLOR_PALETTE[theme_idx][4]
    
    # Guarda la posicion actual del cursor
    solution_coords = [coords for coords, _ in solution_path]
    print("\033[s", end="")
    for x, y in solution_coords:
        # Reestablece el cursor al checkpoint
        print("\033[u", end="")
        
        # Calcula el eje Y vertical y el eje X horizontal
        lines_up = 2 * (maze.height - y)
        cols_right = x * 4 + 2
        
        move_up = f"\033[{lines_up}A"
        move_right = f"\033[{cols_right}C" if cols_right > 0 else ""
        
        # Mueve e imprime sin salto de linea y forzando el flush(necesario)
        print(f"{move_up}{move_right}{sol_color}•{ec}", end="", flush=True)
        time.sleep(0.05)
        
    # Devuelve el curror al punto de partida(posicion final de la impresion)
    print("\033[u", end="")
    print()


def determine_display_mode(
        maze_width: int,
        maze_height: int
        ) -> bool:
    """
    Evaluate terminal values to define forty-two patern
    and animation-mode display
    """

    header_lines = 17
    safety_margin = 2
    render_width = (maze_width * 4) + 1
    render_height = (maze_height * 2) + 1

    term_width, term_height = shutil.get_terminal_size(fallback=(80, 24))
    animated_solution: bool = (render_width + safety_margin <= term_width and
                               render_height + safety_margin + header_lines <= term_height)

    return animated_solution


def display(
        maze: Maze,
        pattern_42: set[tuple[int, int]],
        solution_path: list[tuple[int, int]] | None = None,
        maze_fits: bool = False,
        theme_idx: int = 4,
        random_color: bool = False
    ) -> None:
    """
    Handles the display of the maze and the solution animation if enabled.
     Args:
        maze (Maze): The maze object to be displayed.
        pattern_42 (set[tuple[int, int]]):
        Set of coordinates for the 42 pattern.
        solution_path (list[tuple[int, int]], optional):
        List of coordinates for the solution path. Defaults to None.
        animated_solution (bool, optional):
        Whether to animate the solution path. Defaults to False.
        theme_idx (int, optional):
        Index for the color theme. Defaults to 4.
        random_color (bool, optional):
        Whether to select a random color theme. Defaults to False.
    """
    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "header.txt")

        for c in header_yield(file_path):
            print(c, end="", flush=True)
            time.sleep(0.005)

    except FileNotFoundError as e:
        print(f"Caught an error: {e}")

    print_maze(
        maze,
        pattern_42,
        solution_path,
        maze_fits,
        theme_idx,
        random_color
        )
