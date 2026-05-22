import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import time

R, C = 15, 20
CELL_SIZE = 1.0
WALL_HEIGHT = 0.5

north_wall = [[1 for _ in range(C)] for _ in range(R)]
east_wall  = [[1 for _ in range(C)] for _ in range(R)]

PHASE = "GENERATING"
gen_stack   = []
gen_visited = [[0 for _ in range(C)] for _ in range(R)]

start_node = (random.randint(2, R-3), random.randint(2, C-3))
end_node   = (random.randint(2, R-3), random.randint(2, C-3))
while end_node == start_node:
    end_node = (random.randint(2, R-3), random.randint(2, C-3))

solver_stack    = [start_node]
path_stack      = []
dead_ends       = []
visited_solver  = [[False for _ in range(C)] for _ in range(R)]
current_pos     = start_node
def generate_step():
    global PHASE
    if not gen_stack:
        # ADDENDUM: Create cycles by eating 1 in 20 random walls
        for _ in range(int((R*C)/20)):
            ir, ic = random.randint(1, R-2), random.randint(1, C-2)
            if random.random() > 0.5: north_wall[ir][ic] = 0
            else: east_wall[ir][ic] = 0
        PHASE = "SOLVING"
        return

    r, c = gen_stack[-1]
    gen_visited[r][c] = 1
    cand = []
    if r > 0     and not gen_visited[r-1][c]: cand.append((r-1, c))
    if r < R-1   and not gen_visited[r+1][c]: cand.append((r+1, c))
    if c > 0     and not gen_visited[r][c-1]: cand.append((r, c-1))
    if c < C-1   and not gen_visited[r][c+1]: cand.append((r, c+1))

    if cand:
        nr, nc = random.choice(cand)
        if nr < r:   north_wall[r][c]    = 0
        elif nr > r: north_wall[nr][nc]  = 0
        elif nc < c: east_wall[r][c-1]   = 0
        elif nc > c: east_wall[r][c]     = 0
        gen_visited[nr][nc] = 1
        gen_stack.append((nr, nc))
    else:
        gen_stack.pop()
