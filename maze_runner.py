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
def draw_block(x, y, z, sx, sy, sz, color):
    """Draws a 3D cube/wall."""
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glBegin(GL_QUADS)
    glVertex3f(1,1,-1);  glVertex3f(-1,1,-1);  glVertex3f(-1,1,1);  glVertex3f(1,1,1)   # Top
    glVertex3f(1,-1,1);  glVertex3f(-1,-1,1);  glVertex3f(-1,-1,-1);glVertex3f(1,-1,-1) # Bottom
    glVertex3f(1,1,1);   glVertex3f(-1,1,1);   glVertex3f(-1,-1,1); glVertex3f(1,-1,1)  # Front
    glVertex3f(1,-1,-1); glVertex3f(-1,-1,-1); glVertex3f(-1,1,-1); glVertex3f(1,1,-1)  # Back
    glVertex3f(-1,1,1);  glVertex3f(-1,1,-1);  glVertex3f(-1,-1,-1);glVertex3f(-1,-1,1) # Left
    glVertex3f(1,1,-1);  glVertex3f(1,1,1);    glVertex3f(1,-1,1);  glVertex3f(1,-1,-1) # Right
    glEnd()
    glPopMatrix()

def render_scene():
    """Draws the floor and all walls."""
    off_x = -(C * CELL_SIZE) / 2
    off_z = -(R * CELL_SIZE) / 2
    # Floor
    draw_block(0, -0.05, 0, (C*CELL_SIZE)/2, 0.02, (R*CELL_SIZE)/2, (0.1, 0.1, 0.1))
    for r in range(R):
        for c in range(C):
            x = off_x + c * CELL_SIZE
            z = off_z + r * CELL_SIZE
            if north_wall[r][c]:
                draw_block(x+CELL_SIZE/2, WALL_HEIGHT/2, z,               CELL_SIZE/2, WALL_HEIGHT/2, 0.05, (0.7,0.7,0.7))
            if east_wall[r][c]:
                draw_block(x+CELL_SIZE,   WALL_HEIGHT/2, z+CELL_SIZE/2,   0.05, WALL_HEIGHT/2, CELL_SIZE/2, (0.6,0.6,0.6))
            if c == 0:
                draw_block(x,             WALL_HEIGHT/2, z+CELL_SIZE/2,   0.05, WALL_HEIGHT/2, CELL_SIZE/2, (0.6,0.6,0.6))
            if r == R-1:
                draw_block(x+CELL_SIZE/2, WALL_HEIGHT/2, z+CELL_SIZE,     CELL_SIZE/2, WALL_HEIGHT/2, 0.05, (0.7,0.7,0.7))