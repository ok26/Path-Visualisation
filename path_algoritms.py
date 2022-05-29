import numpy as np 

def dijkstras_algoritm(grid, start, end):
    tentatives = {}
    unvisited = {}

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            tentatives[str(y)+","+str(x)] = float("inf")
            unvisited[str(y)+","+str(x)] = True

    for key in [str(y)+","+str(x) for y,x in zip(np.where(grid==1)[0], np.where(grid==1)[1])]:
        unvisited[key] = False

    tentatives[start] = 0
    current = start

    while unvisited[end] == True and min([tentatives[x] for x in tentatives.keys() if unvisited[x]]) != float("inf"):

        y, x = int(current.split(",")[0]), int(current.split(",")[1])
        sides = []
        for ny in range(y-1,y+2):
            if ny != y and ny >= 0 and ny < len(grid) and unvisited[str(ny)+","+str(x)]:
                sides.append(str(ny)+","+str(x))

        for nx in range(x-1,x+2):
            if nx != x and nx >= 0 and nx < len(grid[0]) and unvisited[str(y)+","+str(nx)]:
                sides.append(str(y)+","+str(nx))

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
        
    if  current != end and min([tentatives[x] for x in tentatives.keys() if unvisited[x]]) == float("inf"):
        return tentatives, False

    else:
        checking = end
        path = [end]
        while tentatives[checking] > 0:
            sides = []
            y, x = int(checking.split(",")[0]), int(checking.split(",")[1])
            for ny in range(y-1,y+2):
                if ny != y and ny >= 0 and ny < len(grid):
                    sides.append(str(ny)+","+str(x))

            for nx in range(x-1,x+2):
                if nx != x and nx >= 0 and nx < len(grid[0]):
                    sides.append(str(y)+","+str(nx))

            smallest_side = sides[[tentatives[side] for side in sides].index(min([tentatives[side] for side in sides]))]
            path.append(smallest_side)
            checking = smallest_side

        path = path[1:-1][::-1]

        return tentatives, path