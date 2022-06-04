import numpy as np
from random import randint
from math import ceil, floor
import matplotlib.pyplot as plt

def recursive_division(grid, maze_ratio=(-1,1)):
    #grid-axis must be divisible by 3
    if len(grid) == 0:
            return grid
    try:
        grid_width = len(grid[0])
        grid_height = len(grid)
    except:
        print(grid, len(grid))

    if grid_width == 0:   #Because bug with empty array thats actually not empty
        return grid

    while True:
        split_on_x = randint(maze_ratio[0],maze_ratio[1])
        if split_on_x > 0:
            split_on_x = 1
            maze_ratio = (maze_ratio[0] - 100, maze_ratio[1])
            break
        elif split_on_x < 0:
            split_on_x = 0
            maze_ratio = (maze_ratio[0], maze_ratio[1] + 100)
            break

    if grid_width < 3 and grid_height >= 3:
        split_on_x = 0
    elif grid_width >= 3 and grid_height < 3:
        split_on_x = 1
    elif grid_width < 3 and grid_height < 3:
        return grid

    if split_on_x:
        grid = np.rot90(grid, k=1)
        grid_width, grid_height = grid_height, grid_width

    y_to_split = randint(ceil(grid_height*0.3),floor((grid_height-1)*0.7))
    if y_to_split % 2 == 0:
        y_to_split += 1

    sub_grid1 = grid[y_to_split+1:,:]
    sub_grid2 = grid[:y_to_split,:]
    grid_ones = grid[y_to_split,:]
    grid_ones[:] = 1

    if split_on_x:
        grid_ones = np.ones((len(grid_ones),1))
        sub_grid1 = np.rot90(sub_grid1, k=-1)
        sub_grid2 = np.rot90(sub_grid2, k=-1)
    
    
    zero_ind = randint(0,len(grid_ones)-1)
    
    if zero_ind % 2 == 1 and len(grid_ones) != 2:
        zero_ind -= 1
    grid_ones[zero_ind] = 0

    if not split_on_x:
        grid_ones = [grid_ones]

    if grid_height <= 3 and grid_width <= 3:
        return np.concatenate((sub_grid1, grid_ones, sub_grid2), axis=split_on_x)

    output_grid = np.concatenate((recursive_division(sub_grid1, maze_ratio), grid_ones, recursive_division(sub_grid2, maze_ratio)), axis=split_on_x)

    return output_grid


def fix_maze_bug(maze):
    for y in range(1,len(maze)-1):
        for x in range(1,len(maze[0])-1):
            check = [x for x in maze[y,x-1:x+2] if x == 1] + [x for x in maze[y-1:y+2,x] if x == 1]
            check_2 = [[x for x in maze[y-1+i,x-1:x+2] if x == 1] for i in range(3)]
            check_2 = check_2[0] + check_2[1] + check_2[2] 

            if maze[y,x] == 0 and len(check) > 2 and len(check) == len(check_2):
                if len(check) == 3:
                   for i in range(3):
                        if i != 1 and maze[y,x-1+i] == 0:
                            maze[y,x] = 1
                            maze[y-1,x] = 0
                            break
                        if i != 1 and maze[y-1+i,x] == 0:
                            maze[y,x] = 1
                            maze[y,x-1] = 0
                            break
                else:
                    total_y = 0
                    total_x = 0
                    sign = -1
                    i = 0

                    while True:
                        if y+(i*sign) >= 0 and y+(i*sign) < len(maze)-1 and maze[y+(i*sign),x] == 1:
                            total_y += 1
                        else:
                            sign = -sign
                            i = 0
                            if sign < 0:
                                break
                        i += 1

                    while True:
                        if x+(i*sign) >= 0 and x+(i*sign) < len(maze[0])-1 and maze[y,x+(i*sign)] == 1:
                            total_x += 1
                        else:
                            sign = -sign
                            i = 0
                            if sign < 0:
                                break
                        i += 1

                    if total_y >= total_x:
                        maze[y,x] = 1
                        maze[y-1,x] = 0
                    else:
                        maze[y,x] = 1
                        maze[y,x-1] = 0
    return maze