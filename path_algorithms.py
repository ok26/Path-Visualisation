import numpy as np 
from math import ceil

def assemble_path(end, dist_values, grid):
    checking = end
    path = [end]
    while dist_values[checking] > 0:
        sides = []
        y, x = int(checking.split(",")[0]), int(checking.split(",")[1])
        for ny in range(y-1,y+2):
            if ny != y and ny >= 0 and ny < len(grid):
                sides.append(str(ny)+","+str(x))

        for nx in range(x-1,x+2):
            if nx != x and nx >= 0 and nx < len(grid[0]):
                sides.append(str(y)+","+str(nx))

        smallest_side = sides[[dist_values[side] if side in dist_values else float("inf") for side in sides].index(min([dist_values[side] if side in dist_values else float("inf") for side in sides]))]
        path.append(smallest_side)
        checking = smallest_side

    path = path[1:-1][::-1]
    return path

def generate_succesors(y,x,grid,visited):
    succesors = []
    for ny in range(y-1,y+2):
        if ny >= 0 and ny < len(grid) and (str(ny)+","+str(x)) not in visited:
            succesors.append(str(ny)+","+str(x))
    for nx in range(x-1,x+2):
        if nx >= 0 and nx < len(grid[0]) and (str(y)+","+str(nx)) not in visited:
            succesors.append(str(y)+","+str(nx))
    return succesors


def visualize_dijkstras_algorithm(grid, start, end, grid_obj):
    output_grid = np.zeros_like(grid)
    counter = 1
    closed_list = {}
    open_list = {}
    walls = np.where(grid==1)

    for key in [str(y)+","+str(x) for y,x in zip(walls[0], walls[1])]:
        closed_list[key] = float("inf")
    
    open_list[start] = 0
    while len(open_list) != 0:
        minv = float("inf")
        for k,v in open_list.items():
            if v < minv:
                minv = v
                mink = k 
        mink_split = mink.split(",")
        x,y = int(mink_split[1]), int(mink_split[0])

        if mink != start and mink != end: 
            output_grid[y,x] = int(ceil(counter/(int((grid_obj.speed_slidebar.get())/10)+1)))
            counter += 1

        closed_list[mink] = open_list[mink]
        del open_list[mink]

        if mink == end:
            path = assemble_path(end, closed_list, grid)
            return output_grid, path, len([x for x in closed_list.values() if x != float("inf")])

        succesors = generate_succesors(y,x,grid,closed_list)
        for succesor in succesors:
            open_list[succesor] = closed_list[mink] + 1
    return output_grid, False, 0


def visualize_A_star(grid, start, end, grid_obj):
    output_grid = np.zeros_like(grid)
    counter = 1
    open_list = {}
    closed_list = {}
    end_x, end_y = int(end.split(",")[1]), int(end.split(",")[0])

    for key in [str(y)+","+str(x) for y,x in zip(np.where(grid==1)[0], np.where(grid==1)[1])]:
        closed_list[key] = [None,float("inf"),None]  #Wall
    
    open_list[start] = [0,0,0]   #f,g,h
    while len(open_list) != 0:
        minv = float("inf")
        for k,v in open_list.items():
            if v[0] < minv:
                minv = v[0]
                mink = k   #q
        x,y = int(mink.split(",")[1]), int(mink.split(",")[0])

        if mink != start and mink != end: 
            output_grid[y,x] = int(ceil(counter/(int((grid_obj.speed_slidebar.get())/10)+1)))
            counter += 1

        closed_list[mink] = open_list[mink]
        del open_list[mink]

        if mink == end:
            for k in closed_list.keys():
                closed_list[k] = closed_list[k][1]
            path = assemble_path(end, closed_list, grid)
            return output_grid, path, len([x for x in closed_list.values() if x != float("inf")])

        succesors = generate_succesors(y,x,grid,closed_list)
        for succesor in succesors:
            suc_x, suc_y = int(succesor.split(",")[1]), int(succesor.split(",")[0])

            g = closed_list[mink][1] + 1
            h = ( abs(end_x-suc_x) + abs(end_y-suc_y) )
            f = g+h
            
            if succesor in open_list and open_list[succesor][0] < f:
                continue
            else:
                open_list[succesor] = [f,g,h]
    return output_grid, False, 0


def visualize_Greedy(grid, start, end, grid_obj):
    output_grid = np.zeros_like(grid)
    counter = 1
    open_list = {}
    closed_list = {}
    end_x, end_y = int(end.split(",")[1]), int(end.split(",")[0])

    for key in [str(y)+","+str(x) for y,x in zip(np.where(grid==1)[0], np.where(grid==1)[1])]:
        closed_list[key] = (None, float("inf"))  #Wall
    
    open_list[start] = (0,0)   #Shortest distance to end, distance travelled so far
    while len(open_list) != 0:
        minv = float("inf")
        for k,v in open_list.items():
            if v[0] < minv:
                minv = v[0]
                mink = k   #q
        x,y = int(mink.split(",")[1]), int(mink.split(",")[0])

        if mink != start and mink != end: 
            output_grid[y,x] = int(ceil(counter/(int((grid_obj.speed_slidebar.get())/10)+1)))
            counter += 1
            
        closed_list[mink] = open_list[mink]
        del open_list[mink]

        if mink == end:
            for k in closed_list.keys():
                closed_list[k] = closed_list[k][1]
            path = assemble_path(end, closed_list, grid)
            return output_grid, path, len([x for x in closed_list.values() if x != float("inf")])

        succesors = generate_succesors(y,x,grid,closed_list)
        for succesor in succesors:
            suc_x, suc_y = int(succesor.split(",")[1]), int(succesor.split(",")[0])

            g = closed_list[mink][1] + 1
            h = ( abs(end_x-suc_x) + abs(end_y-suc_y) )
            
            if succesor in open_list and open_list[succesor][0] < h:
                continue
            else:
                open_list[succesor] = (h,g)
    return output_grid, False, 0