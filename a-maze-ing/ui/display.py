from __future__ import annotations
import os
import random
from typing import Generator
import time
from mazegen import Maze
import shutil

# Color palette: Each theme is a list of ANSI escape codes for background, path, font, pattern, and end color.
COLOR_PALETTE = [
    # 0: bg,           1: path,          2: font,          3: p42,          4: ec
    # night
    ["\033[48;5;17m", "\033[48;5;229m", "\033[38;5;129m", "\033[48;5;51m", "\033[0m"],
    # uzumaki
    ["\033[48;5;166m", "\033[48;5;019m", "\033[38;5;241m", "\033[48;5;220m", "\033[0m"],
    # akatsuki
    ["\033[48;5;233m", "\033[48;5;238m", "\033[38;5;251m", "\033[48;5;124m", "\033[0m"],
    # dark mode
    ["\033[48;5;233m", "\033[48;5;236m", "\033[38;5;241m", "\033[48;5;220m", "\033[0m"],
    # eva01
    ["\033[48;5;128m", "\033[48;5;54m", "\033[38;5;54m", "\033[48;5;76m", "\033[0m"],
    # ox
    ["\033[48;5;55m", "\033[48;5;177m", "\033[38;5;177m", "\033[48;5;99m", "\033[0m"]
]


class DisplayMazeError(Exception):
    """Exception raised for errors in the maze display process."""
    pass


def print_maze(
        maze: Maze,
        pattern_42: set[tuple[int, int]],
        solution_path: list[tuple[int, int]] | None = None,
        #maze_fits: bool = False, ya no es necesario, se determina desde run_visuals()
        #show_solution: bool = False, ya no es necesario, se determina con el menú
        theme_idx: int = 4,
        random_color: bool = False
        ) -> None:
    """
    Prints the maze to the terminal with optional
    styling and solution path.
     Args:
            maze (Maze): The maze object to be printed.
            Pattern_42 (set[tuple[int, int]]): Set of coordinates for the '42' pattern cells.
            solution_path (list[tuple[int, int]], optional): List of coordinates for the solution path. Defaults to None.
            theme_idx (int, optional): Index for the color theme. Defaults to 4.
            random_color (bool, optional): Whether to select a random color theme. Defaults to False.
     Raises:
            DisplayMazeError: If the maze cannot be displayed properly due to terminal size constraints.
    """
    if random_color:
        theme_idx = random.randint(0, len(COLOR_PALETTE) - 1)

    bg = COLOR_PALETTE[theme_idx][0]
    ft = COLOR_PALETTE[theme_idx][3]
    font = COLOR_PALETTE[theme_idx][2]
    path = COLOR_PALETTE[theme_idx][1]
    ec = COLOR_PALETTE[theme_idx][4]

    r_style = bg + font

    # sol_set: set[tuple[int, int]] = (
    #     set(solution_path) if solution_path else set[tuple[int, int]]()
    # )

    top_line = r_style
    # solved_path = [coord for coord, _ in sol_set]

    for x in range(maze.width):
        top_line += "+---"
    top_line += "+" + ec
    print(top_line)

    # for each row of the maze
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
            # mostrar solución instantaneamente ya no es necesario, debe activarse desde menú
            # elif (x, y) in solved_path and not maze_fits and show_solution:
            #     # render solution path
            #     content = path + " • " + ec + r_style
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
        Args:     file_path (str): The path to the file to be read.
        Yields:     Generator[dict, None, None]: A generator that yields characters from the file.
    """
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            for c in line:
                yield c


def header_animation() -> None:
    """
    Displays the header animation by reading the header.txt file and printing its content with a delay.
    """
    try:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "header.txt")

        for c in header_yield(file_path):
            print(c, end="", flush=True)
            time.sleep(0.00005)
            print("\033[s", end="")

    except FileNotFoundError as e:
        print(f"Caught an error: {e}")


# For print over terminal output, we must use print("\033[) with the specific flag:

# 's' saves a checkpoint of the current terminal-cursor position.
# 'u' return the cursor-position to the last checkpoint saved.
# {value} + 'A' moves the terminal-cursor to up direction n_value times.
# {value} + 'C' moves the terminal-cursor to right direction n_value times.

def animation(maze, solution_path: list, theme_idx: int = 4) -> None:
    """
    prints step by step the solution path with a delay between each step.
        Args:
            maze (Maze): The maze object being displayed.
            solution_path (list[tuple[int, int]]): List of coordinates for the solution path.
            theme_idx (int, optional): Index for the color theme. Defaults to 4.
        Raises:
            DisplayMazeError: If the terminal is resized during the animation, which could cause display issues
    """
    sol_color = COLOR_PALETTE[theme_idx][1] 
    ec = COLOR_PALETTE[theme_idx][4]
    # revisa tamaño del terminal al inicio de la animación
    initial_size = shutil.get_terminal_size()
    # Guarda la posicion actual del cursor
    solution_coords = [coords for coords, _ in solution_path]
    print("\033[s", end="")
    for x, y in solution_coords:
        # revisa el tamaño de la terminal en cada iteración,
        # si cambia o es menor al tamaño inicial, termina la animación
        # para evitar errores de impresión
        current_size = shutil.get_terminal_size()
        if current_size != initial_size:
            print("\033[u", end="", flush=True) # Regresa al final
            raise DisplayMazeError("Terminal resized during animation. Returning to safe state.")
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
        
    # Devuelve el cursor al punto de partida(posicion final de la impresion)
    print("\033[u", end="", flush=True) # Regresa al Punto A y SE QUEDA AHÍ

#esta funcion era "determine_display_mode". Ya no es necesario saber
# si puede o no puede imprimirse la solución porque se determina desde run_visuals()
# en este momento la uso para determinar si se puede o no imprimir el laberinto. he quitado el return bool.
def check_display_size(
        maze_width: int,
        maze_height: int
        ) -> None:
    """
    Evaluates the terminal size against the maze dimensions to determine if the maze can be displayed properly.
     Args:
        maze_width (int): The width of the maze.
        maze_height (int): The height of the maze.
    """

    with open("header.txt", encoding='utf-8') as f:
        header_lines = sum(1 for _ in f)
    safety_margin = 3
    menu_lines = 5
    render_width = (maze_width * 4) + 1
    render_height = (maze_height * 2) + 1
    height_needed = (render_height + header_lines + menu_lines + safety_margin)

    term_width, term_height = shutil.get_terminal_size(fallback=(80, 24))
    if term_height < height_needed or term_width < render_width:
        print(f"\033[{header_lines + safety_margin};0H", end="")
        raise DisplayMazeError("Terminal size is too small to display the maze properly." \
        " Please resize your terminal and try again.")


def menu_visuals(theme_idx: int) -> None:
    """Displays the menu options with the current theme colors.
     Args:
        theme_idx (int): The index of the current color theme."""
    
    bg = COLOR_PALETTE[theme_idx][0]
    ft = COLOR_PALETTE[theme_idx][3]
    font = COLOR_PALETTE[theme_idx][2]
    ec = COLOR_PALETTE[theme_idx][4]

    style = f"{bg}{font}"

    print(f"{ft} {font} \nLau&Lau Maze menu: {ec}")
    print(f"Press {style}'R'{ec} to regenerate maze")
    print (f"Press {style}'S'{ec} to toggle solution animation")
    print(f"Press {style}'C'{ec} to change color theme")
    print(f"Press {style}'Q'{ec} to quit")



def display_maze(
        maze: Maze,
        pattern_42: set[tuple[int, int]],
        solution_path: list[tuple[int, int]] | None = None,
        #maze_fits: bool = False, se determina desde run_visuals()
        #instant_solution: bool = False, no es necesario, se determina con el menú
        theme_idx: int = 4,
        random_color: bool = False
    ) -> None:
    """
    Handles the display of the maze in the terminal, including checking if the maze fits within the terminal size ç
    and printing the maze with the appropriate styling.
     Args:
        maze (Maze): The maze object to be displayed.
        pattern_42 (set[tuple[int, int]]): Set of coordinates for the '42' pattern cells.
        solution_path (list[tuple[int, int]], optional): List of coordinates for the solution path. Defaults to None.
        theme_idx (int, optional): Index for the color theme. Defaults to 4.
        random_color (bool, optional): Whether to select a random color theme. Defaults to False.
     Raises:
        DisplayMazeError: If the maze cannot be displayed properly due to terminal size constraints.
    """
    check_display_size(maze.width, maze.height)
    print_maze(
        maze,
        pattern_42,
        solution_path,
        # maze_fits,
        # instant_solution,
        theme_idx,
        random_color
        )
