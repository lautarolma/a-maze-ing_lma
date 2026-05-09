
*This project has been created as part of the 42 curriculum by lospina-, laviles.*

# A-Maze-ing

## Description

A-Maze-ing is a Python-based maze generator and visualizer that creates ASCII art representations of mazes. The project generates perfect mazes using a randomized Kruskal's algorithm, with the option to include a custom "42" pattern. It provides both a command-line interface for maze generation and an interactive visual display with color themes and solution animation.

The goal of this project is to create a reusable maze generation library while providing an engaging visual interface for exploring generated mazes. Users can configure maze dimensions, entry/exit points, and various display options through a simple configuration file.

## Instructions

### Installation

1. Clone or download the project repository.
2. Create a virtual environment (recomended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the package 'mazegen' using the pre-build file (.whl) located in the root of the project:
   ```bash
   pip install mazegen-1.0.0-py3-none-any.whl
   ```

### Execution

To run the maze generator and visualizer:

```bash
python3 a_maze_ing.py config.txt
```

The program will generate the maze, display it with the chosen theme, and save the hexadecimal representation to the specified output file.

### Configuration File Structure

The configuration file uses a simple key=value format. All mandatory keys must be present, and optional keys can be omitted (defaults will be used).

#### Mandatory Keys:
- `WIDTH`: Integer, maze width in cells (5-60)
- `HEIGHT`: Integer, maze height in cells (5-60)
- `ENTRY`: Coordinates in format "x,y" (e.g., "0,0")
- `EXIT`: Coordinates in format "x,y" (e.g., "24,23")
- `OUTPUT_FILE`: String, path to save the hexadecimal maze representation
- `PERFECT`: Boolean ("true" or "false"), whether to generate a perfect maze (default: true)

#### Optional Keys:

- `SEED`: Integer, random seed for reproducible mazes (default: None)


Example config.txt:
```
WIDTH=25
HEIGHT=25
ENTRY=0,0
EXIT=24,23
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Resources

### References
- Kruskal algorithm: https://www.youtube.com/watch?v=OZKuWP1KxdY
- BFS algorithm - https://www.youtube.com/watch?v=4U52GHZS04Q
- ASCII art patterns: https://www.asciiart.eu/ascii-games
- Color palettes: https://upload.wikimedia.org/wikipedia/commons/1/15/Xterm_256color_chart.svg
- jperez-s & josjimen a-maze-ing project: https://github.com/thehuan0/A-Maze-ing

### AI Usage
AI was used in this project:
- Helped with the understanding of complex concepts such as Breadth-First Search (BFS), Graph theory and Spanning trees.
- Helped Write and translate the README.md file of the project
- Helped write and translate the README.md file of the mazegen package
- Helped with debugging specific code sections
- AI was used as a research tool overall

No AI-generated code was directly copied; all implementations are original.

## Reusable Code
The `mazegen` package is designed to be fully reusable:

### Maze Generation Algorithm
We chose **Randomized Kruskal's Algorithm** for maze generation.

**Why this algorithm:**
- Guarantees a perfect maze (single path between any two points)
- Efficient with O(E log E) time complexity where E is the number of edges
- Produces aesthetically pleasing, organic-looking mazes
- Easy to implement with Union-Find data structure
- Allows for reproducible results with seed values

**How it works:**
1. Create a grid of cells, each with four walls
2. Generate all possible walls between adjacent cells
3. Randomly shuffle the list of walls
4. Iterate through walls, removing them if the cells they connect are in different sets (using Union-Find)
5. This creates a spanning tree ensuring all cells are connected without cycles

- **MazeGenerator class**: Can be imported and used independently for maze generation

- **Methods available**:
  - `generate()`: Creates the maze structure
  - `solve()`: Finds the solution path using BFS
  - `get_maze_grid()`: Returns list of int with hex representation of each cell
  - `get_maze_solution()`: Returns list of str with directions N S E W


**The package can be installed via pip and used in other Python projects for maze-related functionality.**

   ```bash
   pip install mazegen-1.0.0-py3-none-any.whl
   ```
   ```bash
   python3
   ```
   ```bash
   from mazegen import MazeGenerator
   ```
   ```bash
   maze = MazeGenerator(
    width=10,
    height=10,
    entry_xy=(0,0),
    exit_xy=(9,9),
    perfect=True,
    Seed=42)
   ```
   ```bash
   maze.generate()
   ```
   ```bash
   maze.solve()
   ```
   ```bash
   grid = maze.get_maze_grid()
   ```
   ```bash
   solution = maze.get_maze_solution()
   ```

## Team roles
**lospina-**

- Core Logic: Designed the initial project architecture and overall logic.
- Kruskal Algorithm and Uion-Find structures implementation.
- Parsing and validator configuration
- Visual: Developed the ASCII visualization, color themes, and display optimization.

**laviles** 

- Advanced Features: Implemented the solution path animation and the logic for non-perfect mazes (braid mazes/loops).
- DevOps & Packaging: Handled the installation flow, environment setup, and Makefile/packaging configuration.
- Quality Assurance: Responsible for general code review and refactoring to meet quality standards.

### Planning and evolution
- Initial plan: research maze algorithms, create project structure, implement core maze generation.
- Next: add configuration parsing and validation, then build terminal UI and animation.
- Final phase: polish output, add optional features, and document the project.

How it evolved:
- The project structure and core generation approach were stable from the start.
- More time was required than expected on pattern-blocking logic and terminal display theming.

### What worked well
- Separation of concerns between generation, configuration, and UI.
- A reusable `mazegen` package for maze-related logic.
- Clear validation and error handling for configuration input.

### What could be improved
- Add support for imperfect maze generation when `PERFECT=false`.
- Add unit tests to validate behavior and catch regressions.
- Improve support for larger maze sizes and better invalid-config feedback.

### Tools Used:
- **Version Control:** Git for source code management
- **Code Quality:** mypy for type checking, flake8 for linting
- **Development Environment:** VS Code with Python extensions
- **Documentation:** Markdown for README and project notes
- **Package Management:** setuptools for Python package creation


