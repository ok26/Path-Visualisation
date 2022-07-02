import numpy as np 
import matplotlib.pyplot as plt
from time import time

def assemble_path(end, dist_values, grid):
    checking = end
    path = [end]
    while dist_values[checking] > 0:
        sides = []
        y, x = checking[0], checking[1]
        for nx in range(x-1,x+2):
            if nx != x and nx >= 0 and nx < len(grid[0]):
                sides.append((y,nx))
        for ny in range(y-1,y+2):
            if ny != y and ny >= 0 and ny < len(grid):
                sides.append((ny,x))

        smallest_side = sides[[dist_values[side] if side in dist_values else float("inf") for side in sides].index(min([dist_values[side] if side in dist_values else float("inf") for side in sides]))]
        path.append(smallest_side)
        checking = smallest_side

    path = path[1:-1][::-1]
    return path

def generate_successors(square,grid,visited=[]):
    y,x = square[0], square[1]
    successors = []
    for nx in range(x-1,x+2):
        if nx >= 0 and nx < len(grid[0]) and (y,nx) not in visited and grid[y,nx] != 1:
            successors.append((y,nx))
    for ny in range(y-1,y+2):
        if ny >= 0 and ny < len(grid) and (ny,x) not in visited and grid[ny,x] != 1:
            successors.append((ny,x))
    return successors

def key_from_smallest_value(dictionary):
    v = list(dictionary.values())
    k = list(dictionary.keys())
    return k[v.index(min(v))]


def visualize_dijkstras_algorithm(grid, start, end):
    output_grid = np.zeros_like(grid)
    counter = 1
    closed_list = {}
    open_list = {}

    open_list[start] = 0
    while len(open_list) != 0:
        mink = key_from_smallest_value(open_list)
        x,y = mink[1], mink[0]

        if mink != start and mink != end: 
            output_grid[y,x] = counter
            counter += 1
            
        closed_list[mink] = open_list[mink]
        del open_list[mink]

        if mink == end:
            path = assemble_path(end, closed_list, grid)
            return output_grid, path, len(closed_list), closed_list

        successors = generate_successors((y,x),grid,closed_list)
        for successor in successors:
            open_list[successor] = closed_list[mink] + 1
    return output_grid, False, len(closed_list), closed_list


def visualize_A_star(grid, start, end):
    output_grid = np.zeros_like(grid)
    counter = 1
    open_list = {}
    closed_list = {}
    end_x, end_y = end[1], end[0]
    
    open_list[start] = [0,0]   #f,g
    while len(open_list) != 0:
        mink = key_from_smallest_value(open_list)
        x,y = mink[1], mink[0]

        if mink != start and mink != end: 
            output_grid[y,x] = counter
            counter += 1

        closed_list[mink] = open_list[mink]
        del open_list[mink]

        if mink == end:
            for k in closed_list.keys():
                closed_list[k] = closed_list[k][1]
            path = assemble_path(end, closed_list, grid)
            return output_grid, path, len(closed_list), closed_list

        successors = generate_successors((y,x),grid,closed_list)
        for successor in successors:
            suc_x, suc_y = successor[1], successor[0]

            g = closed_list[mink][1] + 1
            h = ( abs(end_x-suc_x) + abs(end_y-suc_y))
            f = g+h
            
            if successor in open_list and open_list[successor][0] < f:
                continue
            else:
                open_list[successor] = [f,g]
    for k in closed_list.keys():
        closed_list[k] = closed_list[k][1]
    return output_grid, False, len(closed_list), closed_list


def visualize_Greedy(grid, start, end):
    output_grid = np.zeros_like(grid)
    counter = 1
    open_list = {}
    closed_list = {}
    end_x, end_y = end[1], end[0]

    open_list[start] = (0,0)   #Shortest distance to end, distance travelled so far
    while len(open_list) != 0:
        mink = key_from_smallest_value(open_list)
        x,y = mink[1], mink[0]

        if mink != start and mink != end: 
            output_grid[y,x] = counter
            counter += 1
            
        closed_list[mink] = open_list[mink]
        del open_list[mink]

        if mink == end:
            for k in closed_list.keys():
                closed_list[k] = closed_list[k][1]
            path = assemble_path(end, closed_list, grid)
            return output_grid, path, len(closed_list), closed_list

        successors = generate_successors((y,x),grid,closed_list)
        for successor in successors:
            suc_x, suc_y = successor[1], successor[0]

            g = closed_list[mink][1] + 1
            h = ( abs(end_x-suc_x) + abs(end_y-suc_y) )
            
            if successor in open_list and open_list[successor][0] < h:
                continue
            else:
                open_list[successor] = (h,g)
    for k in closed_list.keys():
        closed_list[k] = closed_list[k][1]
    return output_grid, False, len(closed_list), closed_list


def depth_first(grid, start, end):
    output_grid = np.zeros_like(grid)
    counter = 1
    stack = []
    stack.append((start,0))
    discovered = {}
    while len(stack) > 0:
        (v,d) = stack.pop()
        if v not in discovered:
            discovered[v] = d
            if v != start and v != end:
                output_grid[v[0],v[1]] = counter
                counter += 1
            if v == end:
                return output_grid, assemble_path(end, discovered, grid), len(discovered), discovered
            for successor in generate_successors(v, grid):
                stack.append((successor,d+1))
    return output_grid, False, len(discovered), discovered


def breadth_first(grid, start, end):
    output_grid = np.zeros_like(grid)
    counter = 1
    stack = []
    stack.append(start)
    discovered = {start:0}
    while len(stack) > 0:
        v = stack.pop()
        for successor in generate_successors(v, grid):
            if successor not in discovered:
                discovered[successor] = discovered[v]+1
                stack.append(successor)
                if successor == end:
                    return output_grid, assemble_path(end, discovered, grid), len(discovered), discovered
                if successor != start and successor != end:
                    output_grid[successor[0],successor[1]] = counter
                    counter += 1
    return output_grid, False, len(discovered), discovered
