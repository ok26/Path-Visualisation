import numpy as np
from time import time
from path_algorithms import assemble_path, generate_succesors
from statistics import mean

def A_star_time(loops, grid, start, end):
    times = []
    for i in range(loops):
        start_time = time()
        closed_list = {}
        open_list = {}
        end_coords = end.split(",")
        end_x, end_y = int(end_coords[1]), int(end_coords[0])
        walls = np.where(grid==1)

        for key in [str(y)+","+str(x) for y,x in zip(walls[0], walls[1])]:
            closed_list[key] = [None,float("inf"),None]
        
        open_list[start] = [0,0,0]
        while len(open_list) != 0:
            minv = float("inf")
            for k,v in open_list.items():
                if v[0] < minv:
                    minv = v[0]
                    mink = k   #q
            mink_split = mink.split(",")
            x,y = int(mink_split[1]), int(mink_split[0])
        
            closed_list[mink] = open_list[mink]
            del open_list[mink]

            if mink == end:
                for k in closed_list.keys():
                    closed_list[k] = closed_list[k][1]
                _ = assemble_path(end, closed_list, grid)
                break

            succesors = generate_succesors(y,x,grid,closed_list)
            for succesor in succesors:
                suc_coords = succesor.split(",")
                suc_x, suc_y = int(suc_coords[1]), int(suc_coords[0])

                g = closed_list[mink][1] + 1
                h = ( abs(end_x-suc_x) + abs(end_y-suc_y) )
                f = g+h
                
                if succesor in open_list and open_list[succesor][0] < f:
                    continue
                else:
                    open_list[succesor] = [f,g,h]
        times.append(time()-start_time)
    return mean(times)

def Greedy_time(loops, grid, start, end):
    times = []
    for i in range(loops):
        start_time = time()
        closed_list = {}
        open_list = {}
        end_coords = end.split(",")
        end_x, end_y = int(end_coords[1]), int(end_coords[0])
        walls = np.where(grid==1)

        for key in [str(y)+","+str(x) for y,x in zip(walls[0], walls[1])]:
            closed_list[key] = (None, float("inf"))
        
        open_list[start] = (0,0)
        while len(open_list) != 0:
            minv = float("inf")
            for k,v in open_list.items():
                if v[0] < minv:
                    minv = v[0]
                    mink = k 
            mink_split = mink.split(",")
            x,y = int(mink_split[1]), int(mink_split[0])

            closed_list[mink] = open_list[mink]
            del open_list[mink]

            if mink == end:
                for k in closed_list.keys():
                    closed_list[k] = closed_list[k][1]
                _ = assemble_path(end, closed_list, grid)
                break

            succesors = generate_succesors(y,x,grid,closed_list)
            for succesor in succesors:
                suc_coords = succesor.split(",")
                suc_x, suc_y = int(suc_coords[1]), int(suc_coords[0])

                g = closed_list[mink][1] + 1
                h = ( abs(end_x-suc_x) + abs(end_y-suc_y) )
                
                if succesor in open_list and open_list[succesor][0] < h:
                    continue
                else:
                    open_list[succesor] = (h,g)
        times.append(time()-start_time)
    return mean(times)

def djikstra_time(loops, grid, start, end):
    times = []
    for i in range(loops):
        start_time = time()
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

            closed_list[mink] = open_list[mink]
            del open_list[mink]

            if mink == end:
                _ = assemble_path(end, closed_list, grid)
                break

            succesors = generate_succesors(y,x,grid,closed_list)
            for succesor in succesors:
                open_list[succesor] = closed_list[mink] + 1
        times.append(time()-start_time)
    return mean(times)