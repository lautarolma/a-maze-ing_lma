import random
from collections import deque

class MazeGenerationError(Exception):
    """Custom exception for maze generation errors."""
    pass


# class Cell and methods
class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.parent = self
        self.walls = {"N": True, "S": True, "E": True, "W": True}

    def find(self):
        """find the cell's origin"""
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent

    def union(self, other):
        """
        Merges the set of this cell with the set of the other cell.
    
        Args:
        other (Cell): The neighboring cell with which the merge is performed.
        """
        root1 = self.find()
        root2 = other.find()
        # This avoids cycles
        if root1 != root2:
            root2.parent = root1


# Class Maze and methods
class MazeGenerator:
    DIR_DELTA = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    DIR_CHAR = {'N': 'N', 'S': 'S', 'E': 'E', 'W': 'W'}

    # para iniciar necesita todos los datos del config,
    # se guardan en variables de clase
    def __init__(
            self,
            width: int,
            height: int,
            entry_xy: tuple[int, int],
            exit_xy: tuple[int, int],
            perfect: bool,
            # out_file: str,
            seed: int | None = None) -> None:
        self.width: int = width
        self.height: int = height
        self.entry_xy: tuple[int, int] = entry_xy
        self.exit_xy: tuple[int, int] = exit_xy
        self.perfect: bool = perfect
        # self.out_file: str = out_file
        self.seed: int | None = seed
        self.grid = [[Cell(x, y) for y in range(self.height)]
                     for x in range(self.width)]

    @staticmethod
    def block_42_pattern(width: int, height: int) -> set[tuple[int, int]]:
        """
        blocks 42 pattern cells
        """
        pattern = [
            [1, 0, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
        ox = (width - 7) // 2
        oy = (height - 5) // 2

        cells_to_block: set[tuple[int, int]] = set()
        for r in range(5):
            for c in range(7):
                if pattern[r][c] == 1:
                    cells_to_block.add((ox + c, oy + r))
        return cells_to_block

    def _remove_wall(self, c1: Cell, c2: Cell):
        """
        checks position of two cells and removes walls inbetween

        Args:
        c1, c2 (cell): two cells that are neighbors
        """
        # c1 right c2 left
        if c2.x == c1.x + 1:
            c1.walls["E"] = False
            c2.walls["W"] = False
        # c2 right c1 left
        elif c2.x == c1.x - 1:
            c1.walls["W"] = False
            c2.walls["E"] = False
        # c1 up c2 under
        elif c2.y == c1.y + 1:
            c1.walls["S"] = False
            c2.walls["N"] = False
        # c2 up c1 under
        elif c2.y == c1.y - 1:
            c1.walls["N"] = False
            c2.walls["S"] = False

    def _generate_logic(self):
        pattern_42 = self.block_42_pattern(self.width, self.height)
        walls = []
        for x in range(self.width):
            for y in range(self.height):
                # if the cell is in 42 pattern
                if (x, y) in pattern_42:
                    continue
                if x < self.width - 1:
                    walls.append((self.grid[x][y], self.grid[x+1][y]))
                if y < self.height - 1:
                    walls.append((self.grid[x][y], self.grid[x][y+1]))

        if self.seed is not None:
            random.seed(self.seed)
        random.shuffle(walls)

        for c1, c2 in walls:
            p_42 = False
            if (c1.x, c1.y) in pattern_42:
                p_42 = True
            elif (c2.x, c2.y) in pattern_42:
                p_42 = True
            if not p_42:
                if c1.find() != c2.find():
                    self._remove_wall(c1, c2)
                    c1.union(c2)

    def generate(self):
        """
        generates the maze using randomized Kruskal's algorithm
        """
        self._generate_logic()
        # añadido para probar no_perfect
        # if not self.perfect:
            # romper pardes extra


    # Solve Maze using BFS
    def solve(self) -> list[tuple[Cell, str]]:
        explored: deque[tuple[int, int]] = deque([self.entry_xy])
        origin: dict[tuple[int, int], tuple[tuple[int, int], str] | None] = {self.entry_xy: None}
        while explored:
            cx, cy = explored.popleft()
            if (cx, cy) == self.exit_xy:
                break
            # BFS, checks all posible directions
            for d, (dx, dy) in self.DIR_DELTA.items():
                nx, ny = cx + dx, cy + dy  # moves to first direction (N,S,W,E)
                if (0 <= nx < self.width  # if is on w limit
                    and 0 <= ny < self.height  # if is on h limit
                    and (nx, ny) not in origin  # if the cell have not been explored
                    and not self.grid[cx][cy].walls[d]): # if the wall (ex N) is False
                    origin[(nx, ny)] = ((cx, cy), d) # saves the cell, origin and 'move'
                    explored.append((nx, ny)) # save in explored cells

        if self.exit_xy not in origin:
            raise MazeGenerationError("Exit not found")

        solve_list: list[tuple[Cell, str]] = []
        pos = self.exit_xy
        while origin[pos] is not None:
            info = origin[pos]
            pos = info[0]
            add = pos, info[1]
            solve_list.append(add)

        solve_list.reverse()
        return solve_list

    def hex_maze(self) -> list[str]:
        """
        return hex representation of maze
        """
        hex_str = "0123456789ABCDEF"
        hex_maze = []
        line = ""
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                cell = self.grid[x][y]
                value = 0
                if cell.walls['N']:
                    value += 1
                if cell.walls['E']:
                    value += 2
                if cell.walls['S']:
                    value += 4
                if cell.walls['W']:
                    value += 8
                line += hex_str[value]
            hex_maze.append(line)
        return hex_maze

    def save_to_file(self, filename: str) -> None:
        """
        saves hex representation of maze and solution
        """
        file = filename
        solution = self.solve()
        direction_list = [d for _, d in solution]
        hex_maze = self.hex_maze()
        maze_entry = ",".join(str(i) for i in self.entry_xy)
        maze_exit = ",".join(str(e) for e in self.exit_xy)
        try:
            with open(file, 'w') as f:
                for x_str in hex_maze:
                    line = x_str
                    f.write(line)
                    f.write("\n")
                f.write("\n")
                f.write(maze_entry)
                f.write("\n")
                f.write(maze_exit)
                f.write("\n")
                for d in direction_list:
                    f.write(d)
        except OSError as e:
            print(f"Caught an error generating 'maze.txt' file: {e}")

    def get_maze_grid(self) -> list[list[int]]:
        """
        Gets the maze grid as a 2D list of integers, where each integer
        represents the walls of a cell in hexadecimal format.
        """
        return [
            [int(char, 16) for char in row]
            for row in self.hex_maze()
        ]

    def get_maze_solution(self) -> list[str]:
        """
        Gets the solution to the maze as a list of NSWE directions
        """
        return [d for _, d in self.solve()]
