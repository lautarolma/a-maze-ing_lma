from config import MazeConfigError, ConfigFormat
import random
from collections import deque


# Class Cell and methods
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
        """
        """
        self.width: int = width
        self.height: int = height
        self.entry_xy: tuple[int, int] = entry_xy
        self.exit_xy: tuple[int, int] = exit_xy
        self.perfect: bool = perfect
        # self.out_file: str = out_file
        self.seed: int | None = seed
        self.grid = [[Cell(x, y) for y in range(self.height)]
                     for x in range(self.width)]

    # --- PUBLIC APIS ---
    def generate(self):
        """
        generates the maze using randomized Kruskal's algorithm
        """
        self._generate_logic()
        if not self.perfect:
           self._add_cycles()
           


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
                nx, ny = cx + dx, cy + dy # moves to first direction (N,S,W,E)
                if (0 <= nx < self.width # if is on w limit
                    and 0 <= ny < self.height # if is on h limit
                    and (nx, ny) not in origin # if the cell have not been explored
                    and not self.grid[cx][cy].walls[d]): # if the wall (ex N) is False
                    origin[(nx, ny)] = ((cx, cy), d) # saves the cell, origin and 'move'
                    explored.append((nx, ny)) # save in explored cells

        if self.exit_xy not in origin:
            raise MazeConfigError("Exit not found")

        solve_list: list[tuple[Cell, str]] = []
        pos = self.exit_xy
        while origin[pos] is not None:
            info = origin[pos]
            pos = info[0]
            add = pos, info[1]
            solve_list.append(add)

        solve_list.reverse()
        return solve_list

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
    
    # --- PRIVATE GENERATION LOGICS ---
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

    def _add_cycles(self) -> None:
        """Inyection of cycles to the maze structure"""
        pattern_42 = self.block_42_pattern(self.width, self.height)
        intact_walls: list[tuple[Cell, Cell, str, str]] = []
        
        for x in range(self.width):
            for y in range(self.height):
                c1 = self.grid[x][y]
                if (c1.x, c1.y) in pattern_42:
                    continue

                #Checking east-neighbor 
                if x < self.width - 1 and c1.walls['E']:
                    c2 = self.grid[x+1][y]
                    if (c2.x, c2.y) not in pattern_42:
                        intact_walls.append((c1, c2, 'E', 'W'))

                #Checking south-neighbor
                if y < self.height - 1 and c1.walls['S']:
                    c2 = self.grid[x][y+1]
                    if (c2.x, c2.y) not in pattern_42:
                        intact_walls.append((c1, c2, 'S', 'N'))
            
        # Avoiding localized cycles.        
        random.shuffle(intact_walls)

        # Breaking walls simulations
        for (c1, c2, wall1, wall2) in intact_walls:
            c1.walls[wall1] = False
            c2.walls[wall2] = False

            creates_3x3: bool = False

            # Defines possible 3x3 blocks origins from reference cells
            for (sx, sy) in self._fetch_3x3_origin(c1, c2):
                if self._is_3x3_open(sx, sy):
                    creates_3x3 = True
                    break

            # If it fail, walls are restored
            if creates_3x3:
                c1.walls[wall1] = True
                c2.walls[wall2] = True

    # --- UTILITIES/HELPERS ---
    def hex_maze(self) -> list[str]:
        """Return hex representation of maze."""
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

    def _is_3x3_open(self, sx, sy) -> bool:
        "Validates area looking for 3x3 open areas"
        #Checking on vertical walls
        for x in range(sx, sx + 2):
            for y in range(sy, sy + 3):
                if self.grid[x][y].walls['E']:
                    return False

        #Checking on horizontal walls
        for x in range(sx, sx + 3):
            for y in range(sy, sy + 2):
                if self.grid[x][y].walls['S']:
                    return False
        # At this point its a full open 3x3 block
        return True

 
    
    def _fetch_3x3_origin(self, c1, c2) -> Cell:
        "Returns the posibles rooth cell/origins of the 3x3 area creations"
        #For vertical walls
        if c1.x != c2.x:
            min_x = min(c1.x, c2.x)
            range_x = (min_x - 1, min_x)
            range_y = (c1.y - 2, c1.y - 1, c1.y)
        
        #For horizontal walls
        else:
            min_y = min(c1.y, c2.y)
            range_x = (c1.x - 2, c1.x - 1, c1.x)
            range_y = (min_y - 1, min_y)

        #Filtering blocks that fit into the maze
        for sx in range_x:
            for sy in range_y:
                #Bounds cheking
                if 0 < sx < self.width - 3 and 0 < sy <= self.height - 3:
                    yield sx, sy
            
