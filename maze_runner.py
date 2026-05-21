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