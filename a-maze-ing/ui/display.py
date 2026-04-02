import os
from typing import Generator
import time
from mazegen import Maze, Cell

# Estilos
COLOR_PALETTE = [
    # 0: bg,           1: path,          2: font,          3: p42,          4: ec
    # night
    ["\033[48;5;17m", "\033[48;5;229m", "\033[38;5;195m", "\033[48;5;51m", "\033[0m"],
    # dark mode
    ["\033[48;5;233m", "\033[48;5;236m", "\033[38;5;236m", "\033[48;5;220m", "\033[0m"],
    # satoru
    ["\033[48;5;255m", "\033[48;5;235m", "\033[38;5;146m", "\033[48;5;45m", "\033[0m"],
    # akatsuki
    ["\033[48;5;233m", "\033[48;5;251m", "\033[38;5;251m", "\033[48;5;124m", "\033[0m"],
    # eva01
    ["\033[48;5;128m", "\033[48;5;54m", "\033[38;5;54m", "\033[48;5;76m", "\033[0m"],
    # uzumaki
    ["\033[48;5;208m", "\033[48;5;220m", "\033[38;5;238m", "\033[48;5;238m", "\033[0m"],
    # ox
    ["\033[48;5;55m", "\033[48;5;177m", "\033[38;5;177m", "\033[48;5;99m", "\033[0m"]
]

# print maze
def print_maze_st(maze, pattern_42: set):
    bg = COLOR_PALETTE[0][0]
    ft = COLOR_PALETTE[0][3]
    font = COLOR_PALETTE[0][2]
    path = COLOR_PALETTE[0][1]
    ec = COLOR_PALETTE[0][4]

    r_style = bg + font

    # 🔹 Línea superior inicial
    top_line = r_style
    for x in range(maze.width):
        top_line += "+---"
    top_line += "+" + ec
    print(top_line)

    # 🔹 Por cada fila del maze
    for y in range(maze.height):

        # 👉 Línea de celdas (verticales)
        line_cells = r_style + "|"

        # 👉 Línea inferior (horizontales)
        line_bottom = r_style

        for x in range(maze.width):
            cell = maze.grid[x][y]

            # ===== CONTENIDO DE LA CELDA =====
            if (x, y) == maze.entry_xy or (x, y) == maze.exit_xy:
                content = path + " * " + ec + r_style
            elif (x, y) in pattern_42:
                content = ft + " * " + ec + r_style
            else:
                content = "   "

            # ===== PARED ESTE =====
            east_wall = "|" if cell.walls["E"] else " "

            # Construir línea de celdas
            line_cells += content + east_wall

            # ===== PARED SUR =====
            if cell.walls["S"]:
                line_bottom += "+---"
            else:
                line_bottom += "+   "

        # cerrar líneas
        line_cells += ec
        line_bottom += "+" + ec

        # imprimir ambas
        print(line_cells)
        print(line_bottom)


def header_yield(file_path: str) ->Generator[dict, None, None]:
    """
    """
    with open(file_path) as f:
        for line in f:
           for c in line:
                yield c



def display(maze, pattern_42: set) -> None:
    """
    """
    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "header.txt")

        for c in header_yield(file_path):
            print(c, end="", flush=True)
            time.sleep(0.005)

    except FileNotFoundError as e:
        print(f"Caught an error: {e}")

    print_maze_st(maze, pattern_42)