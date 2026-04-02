from config.parser import parse_config, ConfigFormat
import random
from collections import deque
from typing import Optional, Tuple, List, Dict


# class Cell and methods
class Cell:
    def __init__(self, x, y):
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
        if root1 != root2:
            root2.parent = root1


# Class Maze and methods
class Maze:
    DIR_DELTA = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    DIR_CHAR = {'N': 'N', 'S': 'S', 'E': 'E', 'W': 'W'}

    def __init__(self, data: ConfigFormat):
        self.width: int = data['width']
        self.height: int = data['height']
        self.entry_xy: tuple[int, int] = data['entry']
        self.exit_xy: tuple[int, int] = data['exit']
        self.perfect: bool = data['perfect']
        self.out_file: str = data['output_file']
        self.seed: Optional[int] = data.get('seed')
        self.grid = [[Cell(x, y) for y in range(self.height)]
                     for x in range(self.width)]
        
    def _block_42_pattern(self):
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
        ox = (self.width - 7) // 2
        oy = (self.height - 5) // 2
        
        cells_to_block = set()
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

    def _generate_maze(self):
        pattern_42 = self._block_42_pattern()
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

    # Solve Maze using BFS
    def solve(self) -> List[str]:
        explored: deque[Tuple[int, int]] = deque([self.entry_xy])
        origin: Dict[Tuple[int, int], Optional
                     [Tuple[Tuple[int, int], str]]] = {self.entry_xy: None}
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
            return []

        path: List[str] = []
        pos = self.exit_xy
        while origin[pos] is not None:
            info = origin[pos]
            path.append(info[1])
            pos = info[0]
        return path[::-1]  # de entrada a salida
    
    def hex_maze(self) -> List[str]:
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

    def save_to_file(self):
        """
        saves hex representation of maze and solution
        """
        file = "maze.txt"
        solution = self.solve()
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
                for D in solution:
                    f.write(D)
        except OSError as e:
            print(f"Caught an error generating 'maze.txt' file: {e}")
    
    
