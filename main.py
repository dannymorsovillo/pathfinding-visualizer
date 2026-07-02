# visualizer for shortest path algos without classes and OOP
# created by danny morsovillo
import heapq
import math
import pygame
from pygame.locals import *

# color constants
DARK_BLUE = (40, 44, 52)
BLUE = (0, 0, 255)
RED = (250, 0, 0)
GREEN = (0, 255, 0)
MAGENTA = (200, 0, 200)
EMPTY = (60, 66, 78)


# dimension constants
# can use as GRID_SIZE / GRID_SIZE since WINDOW_SIZE is currently square
MARGIN = 4
GRID_SIZE = 20
TILE_SIZE = 20
CELL = TILE_SIZE + MARGIN
WINDOW_SIZE = GRID_SIZE * CELL + MARGIN   # window is exactly as big as the grid
MAX_CLICKS = 2

# data structures
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
deltas = [
    (0, 1), (0, -1), (1, 0), (-1, 0),       # orthogonal: right, left, down, up
    (1, 1), (1, -1), (-1, 1), (-1, -1),     # diagonal: corners
]
row = 0
col = 0

# screen initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))


def draw_board():
    start = None
    target = None
    path = []
    graph = {}
    count = 0
    algo = check_user_input()
    running = True
    while running:
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
                running = False

           elif event.type == pygame.MOUSEBUTTONDOWN:
                if count < MAX_CLICKS:
                    pos = pygame.mouse.get_pos()
                    count += 1
                    column = (pos[0] - MARGIN) // (TILE_SIZE + MARGIN)
                    row = (pos[1] - MARGIN) // (TILE_SIZE + MARGIN)
                    if 0 <= row < GRID_SIZE and 0 <= column < GRID_SIZE:
                        cell = (row, column)
                        if start is None:
                            start = cell
                        elif target is None:
                            target = cell
                        else:
                            grid[row][column] = 1 if grid[row][column] == 0 else 0

           elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                graph = build_graph()
                if algo == 'dijkstra':
                    path, total = dih(start, target, graph)
                    print(total)
                elif algo == 'a*':
                    path, total = a_star(start, target, graph)
                    print(total)

        screen.fill(DARK_BLUE)
        draw_path(screen, start, target, path)
        pygame.display.flip()

    pygame.quit()

def check_user_input():
    algo = input('Select an algorithm to visualize (dijkstra or a*): ')
    return algo
        

# dijkstra
def dih(src, target, graph):
    cost_list = {v: float('inf') for v in graph}
    prev = {v: None for v in graph} 
    cost_list[src] = 0
    pq = [(0, src)] # cost, vertex
    vis = set()

    while pq:
        cost, vertex = heapq.heappop(pq)
        if vertex in vis:
            continue
        vis.add(vertex)
        if vertex == target:
            break

        for neighbor, weight in graph[vertex]:
            if neighbor in vis:
                continue
            new_cost = cost + weight
            if new_cost < cost_list[neighbor]:
                cost_list[neighbor] = new_cost
                prev[neighbor] = vertex
                heapq.heappush(pq, (new_cost, neighbor))

    path = []
    node = target
    rebuild_path(path, node, prev, cost_list, target)
    return path, cost_list[target]

# A*
def a_star(src, target, graph):
    g = {v: float('inf') for v in graph}
    g[src] = 0

    #f = g + h
    f = {v: float('inf') for v in graph}
    f[src] = h(src, target)

    pq = [(f[src],src)] #cost, vertex
    prev = {v: None for v in graph} 
    vis = set()

    while pq:
        _, vertex = heapq.heappop(pq)
        if vertex in vis:
            continue
        vis.add(vertex)
        if vertex == target:
            break
            
        for neighbor, weight in graph[vertex]:
            if neighbor in vis:
                continue
            new_g = g[vertex] + weight
            if new_g < g[neighbor]:
                g[neighbor] = new_g
                f[neighbor] = new_g + h(neighbor, target)
                prev[neighbor] = vertex
                heapq.heappush(pq, (f[neighbor], neighbor))
    path = []
    node = target
    rebuild_path(path, node, prev, g, target)
    return path, f[target]
  

#Euclidean distance heurisitc
def h(p, q):
    return math.dist(p, q)


def rebuild_path(path, node, prev, cost, target):
    if cost[target] != float('inf'):
        while node:
            path.append(node)
            node = prev[node]
        path.reverse()



def draw_path(screen, start, target, path):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 1: color = BLUE
            elif (row, col) == start: color = GREEN
            elif (row, col) == target: color = MAGENTA
            elif (row, col) in path: color = RED
            else: color = EMPTY
            pygame.draw.rect(screen, color, [(MARGIN + TILE_SIZE) * col + MARGIN, (MARGIN + TILE_SIZE) * row + MARGIN, TILE_SIZE, TILE_SIZE])


def build_graph():
    graph = {}
    weight = 0
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 1:
                continue
            graph[(r,c)] = []
            for delta_r, delta_c in deltas:
                neighbor_r = delta_r + r
                neighbor_c = delta_c + c
                
                if 0 <= neighbor_r < GRID_SIZE and 0 <= neighbor_c < GRID_SIZE and grid[neighbor_r][neighbor_c] != 1:
                    if delta_c == 0 or delta_r == 0:
                        weight = 1
                    else:
                        weight = 1.414
                    graph[(r,c)].append(((neighbor_r, neighbor_c), weight))
    return graph

def main():
    draw_board()

if __name__ == "__main__":
    main()



         