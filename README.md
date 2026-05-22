# Running-Maze
 
A real-time 3D maze generator and solver built with Python, OpenGL, and GLFW. Watch a maze get carved out using recursive backtracking, then follow a solver as it navigates from start to finish using depth-first search with backtracking.
 
---
 
## Features
 
- **Procedural maze generation** via recursive backtracking (DFS)
- **Animated solving** with visible path tracking and dead-end marking
- **3D perspective rendering** using OpenGL with a tilted top-down camera
- **Randomized cycles** — a small number of walls are removed post-generation to create loops and multiple possible paths
- **Color-coded visualization:**
  - 🟩 Green — start cell
  - 🟨 Gold — end cell
  - 🟥 Red — the solver (current position)
  - ⬜ White — active path (footprints)
  - 🟦 Blue — dead ends (backtracked cells)
---
 
## Requirements
 
- Python 3.7+
- [PyOpenGL](https://pypi.org/project/PyOpenGL/)
- [glfw](https://pypi.org/project/glfw/)
Install dependencies:
 
```bash
pip install PyOpenGL PyOpenGL_accelerate glfw
```
 
---
 
## Usage
 
```bash
python maze.py
```
 
A 1200×900 window will open. The simulation runs in two automatic phases:
 
1. **Generating** — the maze is carved cell by cell; walls appear as the algorithm visits each cell
2. **Solving** — the solver explores the maze, marking its path in white and dead ends in blue until it reaches the gold cell
No interaction is required — just watch.
 
---
 
## Configuration
 
At the top of `maze.py`, you can adjust these constants:
 
| Variable | Default | Description |
|---|---|---|
| `R` | `15` | Number of rows in the maze |
| `C` | `20` | Number of columns in the maze |
| `CELL_SIZE` | `1.0` | Size of each cell in world units |
| `WALL_HEIGHT` | `0.5` | Height of rendered walls |
 
The start and end nodes are placed randomly in the interior of the maze (avoiding the outer border) each run.
 
---
 
## How It Works
 
### Generation — Recursive Backtracking
 
Starting from the `start_node`, the algorithm maintains a stack of visited cells. At each step it picks an unvisited neighbor at random, removes the wall between them, and pushes the neighbor onto the stack. When a cell has no unvisited neighbors, it backtracks. This produces a perfect maze (exactly one path between any two cells).
 
After generation, roughly 1 in 20 interior walls are randomly removed to introduce cycles and make solving more interesting.
 
### Solving — Depth-First Search with Backtracking
 
The solver uses its own stack starting from `start_node`. At each step it tries to move to an unvisited adjacent cell that isn't blocked by a wall. If no such move exists, the current cell is marked a dead end (blue) and the solver backtracks. The active path is tracked in `path_stack` and rendered as white footprints.
 
---
 
## Project Structure
 
```
maze.py          # Single-file implementation
README.md        # This file
```
 
