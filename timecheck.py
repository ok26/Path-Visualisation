import numpy as np
from time import time
from pathfinding_algorithms import assemble_path, generate_successors, key_from_smallest_value
from statistics import mean

def A_star_time(loops, grid, start, end):
    times = []
    for _ in range(loops):
        start_time = time()
        closed_list = {}
        open_list = {}
        open_list[start] = (0,0)

        while len(open_list) != 0:
            mink = key_from_smallest_value(open_list)
            closed_list[mink] = open_list[mink]
            del open_list[mink]

            if mink == end:
                for k in closed_list.keys():
                    closed_list[k] = closed_list[k][1]
                assemble_path(end, closed_list, grid)
                break

            successors = generate_successors(mink,grid,closed_list)
            for successor in successors:
                g = closed_list[mink][1] + 1
                h = ( abs(end[1]-successor[1]) + abs(end[0]-successor[0]) )
                f = g+h
                open_list[successor] = (f,g)
        times.append(time()-start_time)
    return mean(times)

def Greedy_time(loops, grid, start, end):
    times = []
    for _ in range(loops):
        start_time = time()
        closed_list = {}
        open_list = {}
        open_list[start] = (0,0)

        while len(open_list) != 0:
            mink = key_from_smallest_value(open_list)
            closed_list[mink] = open_list[mink]
            del open_list[mink]

            if mink == end:
                for k in closed_list.keys():
                    closed_list[k] = closed_list[k][1]
                assemble_path(end, closed_list, grid)
                break

            successors = generate_successors(mink,grid,closed_list)
            for successor in successors:
                g = closed_list[mink][1] + 1
                h = ( abs(end[1]-successor[1]) + abs(end[0]-successor[0]) )
                open_list[successor] = (h,g)
        times.append(time()-start_time)
    return mean(times)

def djikstra_time(loops, grid, start, end):
    times = []
    for _ in range(loops):
        start_time = time()
        closed_list = {}
        open_list = {}
        open_list[start] = 0

        while len(open_list) != 0:
            mink = key_from_smallest_value(open_list)
            closed_list[mink] = open_list[mink]
            del open_list[mink]

            if mink == end:
                assemble_path(end, closed_list, grid)
                break

            successors = generate_successors(mink,grid,closed_list)
            for successor in successors:
                open_list[successor] = closed_list[mink] + 1
        times.append(time()-start_time)
    return mean(times)

def depth_first_time(loops, grid, start, end):
    times = []
    for _ in range(loops):
        start_time = time()
        stack = []
        stack.append((start,0))
        discovered = {}
        while len(stack) > 0:
            (v,d) = stack.pop()
            if v not in discovered:
                discovered[v] = d
                if v == end:
                    assemble_path(end, discovered, grid)
                    break
                for successor in generate_successors(v, grid):
                    stack.append((successor,d+1))
        times.append(time()-start_time)
    return mean(times)

def breadth_first_time(loops, grid, start, end):
    times = []
    for i in range(loops):
        start_time = time()
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
                        assemble_path(end, discovered, grid)
                        stack = []
                        break
        times.append(time()-start_time)
    return mean(times)
