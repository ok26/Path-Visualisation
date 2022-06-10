import numpy as np 
from time import sleep


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


def visualize_dijkstras_algorithm(grid, start, end, grid_obj, bidirectional, update):
    tentatives = {}
    unvisited = {}
    counter = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            tentatives[str(y)+","+str(x)] = float("inf")
            unvisited[str(y)+","+str(x)] = True

    for key in [str(y)+","+str(x) for y,x in zip(np.where(grid==1)[0], np.where(grid==1)[1])]:
        unvisited[key] = False

    tentatives[start] = 0
    current = start
    grid_obj.current_color = 5
    while unvisited[end] == True and min([tentatives[x] for x in tentatives.keys() if unvisited[x]]) != float("inf") and grid_obj.cancel_algorithm==False:
        y, x = int(current.split(",")[0]), int(current.split(",")[1])
        sides = []
        for ny in range(y-1,y+2):
            if ny != y and ny >= 0 and ny < len(grid) and unvisited[str(ny)+","+str(x)]:
                sides.append(str(ny)+","+str(x))

        for nx in range(x-1,x+2):
            if nx != x and nx >= 0 and nx < len(grid[0]) and unvisited[str(y)+","+str(nx)]:
                sides.append(str(y)+","+str(nx))

        #Displays on canvas, does not work properly, fix in future
        if current != start and current != end:
            if counter == int(grid_obj.speed_slidebar.get()/10):
                if update:
                    grid_obj.canvas.update_idletasks()
                sleep(0.03)
                counter = 0
            else:
                counter += 1
            if bidirectional and grid_obj.np_grid[int(current.split(",")[0]), int(current.split(",")[1])] == 5:
                path = assemble_path(current, tentatives, grid)
                return path, len([v for k,v in tentatives.items() if v != float("inf") and not unvisited[k]])

            grid_obj.fill_square(int(current.split(",")[1]), int(current.split(",")[0]))


        alt = tentatives[current] + 1
        for side in sides:
            if alt < tentatives[side]:
                tentatives[side] = alt
        unvisited[current] = False
        smallest = float("inf")
        for k, v in tentatives.items():
            if unvisited[k] and v < smallest:
                smallest = v
                smallest_key = k

        try:
            if current != end:
                current = smallest_key
        except UnboundLocalError:   #If start surrounded by walls
            pass

    if grid_obj.cancel_algorithm:
        return [], 0
        
    if  current != end and min([tentatives[x] for x in tentatives.keys() if unvisited[x]]) == float("inf"):
        return False, 0

    else:
        path = assemble_path(end, tentatives, grid)
        return path, len([v for k,v in tentatives.items() if v != float("inf") and not unvisited[k]])



def visualize_A_star(grid, start, end, grid_obj, bidirectional, update):
    counter = 0
    unvisited = {}  #open list
    visited = {}  #closed list
    end_x, end_y = int(end.split(",")[1]), int(end.split(",")[0])

    for key in [str(y)+","+str(x) for y,x in zip(np.where(grid==1)[0], np.where(grid==1)[1])]:
        visited[key] = [None,float("inf"),None]  #Wall
    
    unvisited[start] = [0,0,0]   #f,g,h
    grid_obj.current_color = 5
    while len(unvisited) != 0 and grid_obj.cancel_algorithm==False:
        minv = float("inf")
        for k,v in unvisited.items():
            if v[0] < minv:
                minv = v[0]
                mink = k   #q
        x,y = int(mink.split(",")[1]), int(mink.split(",")[0])

        if mink != start and mink != end: 
            if counter == int(grid_obj.speed_slidebar.get()/10):
                if update:
                    grid_obj.canvas.update_idletasks()
                sleep(0.03)
                counter = 0
            else:
                counter += 1
            if bidirectional and grid_obj.np_grid[int(mink.split(",")[0]), int(mink.split(",")[1])] == 5:
                visited[mink] = unvisited[mink]
                for k in visited.keys():
                    visited[k] = visited[k][1]
                path = assemble_path(mink, visited, grid)
                return path, len([v for v in visited.values() if v != float("inf")])
            grid_obj.fill_square(x, y)

        visited[mink] = unvisited[mink]
        del unvisited[mink]

        if mink == end:
            grid_obj.current_color = 4
            for k in visited.keys():
                visited[k] = visited[k][1]
            path = assemble_path(end, visited, grid)
            return path, len([x for x in visited.values() if x != float("inf")])

        succesors = []
        for ny in range(y-1,y+2):
            for nx in range(x-1,x+2):
                if ny >= 0 and ny < len(grid) and nx >= 0 and nx < len(grid[0]) and not(ny==y and nx==x) and (str(ny)+","+str(nx)) not in visited and (nx==x or ny==y):
                    succesors.append(str(ny)+","+str(nx))

        for succesor in succesors:
            suc_x, suc_y = int(succesor.split(",")[1]), int(succesor.split(",")[0])

            g = visited[mink][1] + 1
            h = ( abs(end_x-suc_x) + abs(end_y-suc_y) )
            f = g+h
            
            side_square = ((suc_x-x),(suc_y-y))                     #Checking if diagonal goes through walls
            side_square1 = str(y+side_square[1])+","+str(x)
            side_square2 = str(y)+","+str(x+side_square[0])

            if side_square1 in visited and side_square2 in visited and visited[side_square1][1]==float("inf") and visited[side_square2][1]==float("inf"):
                continue 
            elif succesor in unvisited and unvisited[succesor][0] < f:
                continue
            else:
                unvisited[succesor] = [f,g,h]
    if grid_obj.cancel_algorithm:
        return [], 0
    return False, 0



def visualize_Greedy(grid, start, end, grid_obj, bidirectional, update):
    counter = 0
    unvisited = {}  #open list
    visited = {}  #closed list
    end_x, end_y = int(end.split(",")[1]), int(end.split(",")[0])

    for key in [str(y)+","+str(x) for y,x in zip(np.where(grid==1)[0], np.where(grid==1)[1])]:
        visited[key] = (None, float("inf"))  #Wall
    
    unvisited[start] = (0,0)   #Shortest distance to end, distance travelled so far
    grid_obj.current_color = 5
    while len(unvisited) != 0 and grid_obj.cancel_algorithm==False:
        minv = float("inf")
        for k,v in unvisited.items():
            if v[0] < minv:
                minv = v[0]
                mink = k   #q
        x,y = int(mink.split(",")[1]), int(mink.split(",")[0])

        if mink != start and mink != end: 
            grid_obj.fill_square(x, y)
            if counter == int(grid_obj.speed_slidebar.get()/10):
                grid_obj.canvas.update_idletasks()
                sleep(0.03)
                counter = 0
            else:
                counter += 1
            
        visited[mink] = unvisited[mink]
        del unvisited[mink]

        if mink == end:
                grid_obj.current_color = 4
                for k in visited.keys():
                    visited[k] = visited[k][1]
                path = assemble_path(end, visited, grid)
                return path, len([x for x in visited.values() if x != float("inf")])

        succesors = []
        for ny in range(y-1,y+2):
            for nx in range(x-1,x+2):
                if ny >= 0 and ny < len(grid) and nx >= 0 and nx < len(grid[0]) and not(ny==y and nx==x) and (str(ny)+","+str(nx)) not in visited and (nx==x or ny==y):
                    succesors.append(str(ny)+","+str(nx))

        for succesor in succesors:
            suc_x, suc_y = int(succesor.split(",")[1]), int(succesor.split(",")[0])
            dist = 2
            if x==suc_x or y==suc_y:
                dist = 1

            g = visited[mink][1] + dist
            h = ( abs(end_x-suc_x) + abs(end_y-suc_y) )
            
            if succesor in unvisited and unvisited[succesor][0] < h:
                continue
            else:
                unvisited[succesor] = (h,g)
    if grid_obj.cancel_algorithm:
        return [], 0
    return False, 0