from time import sleep
import tkinter as tk
from math import floor, ceil
from tkinter import messagebox   #Because visualstudio error even when star import
import numpy as np
from tkinter import *
from maze_gen import recursive_division, fix_maze_bug
from path_algorithms import visualize_dijkstras_algorithm, visualize_A_star
import matplotlib.pyplot as plt


class Grid():

    def __init__(self, canvas_width, canvas_height, grid_ind, colors):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.grid_ind = grid_ind
        self.colors = colors
        self.current_color = 1
        self.removing = False
        self.filled_squares = {}
        self.grid_lines = []
        self.size_slidebar = Scale(box1, from_=0, to=20, orient=HORIZONTAL, command=self.resize_grid)
        self.size_slidebar.set(10)
        self.speed_slidebar = Scale(box2, from_=0, to=100, orient=HORIZONTAL)
        self.speed_slidebar.set(60)
   
        self.current_path_algorithm = IntVar()
        self.current_maze_algorithm = IntVar()
        
        self.canvas = tk.Canvas(root, height=canvas_height, width=canvas_width, bg='white')
        self.canvas.bind("<Button>", self.check_mouse_type)
        self.canvas.bind("<B1-Motion>", self.check_mouse_type)
    

    def check_mouse_type(self, event):
        if event.num == 1:
            self.check_square(event)
        elif event.num == 3:
            pass
        elif event.num not in [1,2,3,4,5]:
            self.check_square(event)
        
        
    def create_grid(self):
        grid_width = ((self.canvas_width-2*self.grid_ind)//self.square_side)*self.square_side
        grid_height = ((self.canvas_height-2*self.grid_ind)//self.square_side)*self.square_side

        for i in range(self.grid_ind, self.grid_ind+grid_width+1, self.square_side):
            self.grid_lines.append(self.canvas.create_line([(i, self.grid_ind), (i, self.grid_ind+grid_height)], tag='grid_line'))

        for i in range(self.grid_ind, self.grid_ind+grid_height+1, self.square_side):
            self.grid_lines.append(self.canvas.create_line([(self.grid_ind, i), (self.grid_ind+grid_width, i)], tag='grid_line'))

    
    def check_square(self, event):
        x = event.x
        y = event.y

        if not (x <= self.grid_ind or x >= (self.canvas_squares[1]*self.square_side+self.grid_ind) or y <= self.grid_ind or y >= (self.canvas_squares[0]*self.square_side+self.grid_ind)):

            SquareX = floor((x-self.grid_ind)/(self.square_side))
            SquareY = floor((y-self.grid_ind)/(self.square_side))

            if not self.np_grid[SquareY, SquareX] and not self.removing:
                self.fill_square(SquareX, SquareY)

            elif self.removing and self.np_grid[SquareY, SquareX] != 0:
                self.remove_square(SquareX, SquareY)
            

    def fill_square(self, SquareX, SquareY):
        self.filled_squares[str(SquareX)+","+str(SquareY)] = self.canvas.create_rectangle(SquareX * self.square_side + self.grid_ind, 
                                                                                          SquareY * self.square_side + self.grid_ind, 
                                                                                          SquareX * self.square_side + self.grid_ind + self.square_side, 
                                                                                          SquareY * self.square_side + self.grid_ind + self.square_side, 
                                                                                          fill=self.colors[self.current_color-1])
        self.np_grid[SquareY, SquareX] = self.current_color
        if self.current_color > 1 and self.current_color < 4:
            self.chose_start_stop()

    
    def remove_square(self, SquareX, SquareY):
        if self.np_grid[SquareY, SquareX] == 2 or self.np_grid[SquareY, SquareX] == 3:
            new = messagebox.askyesno("Reset", "Delete Start and Stop Squares?")
            if new:
                self.canvas.delete(self.filled_squares[str(SquareX)+","+str(SquareY)])
                self.np_grid[SquareY, SquareX] = 0
                Second_square = np.where((self.np_grid == 2) | (self.np_grid == 3))
                self.canvas.delete(self.filled_squares[str(Second_square[1][0])+","+str(Second_square[0][0])])
                self.np_grid[Second_square] = 0
                if len(np.where( self.np_grid == 4 )) > 0:
                    self.remove_found_path()

        elif self.np_grid[SquareY, SquareX] == 4 or self.np_grid[SquareY, SquareX] == 5:
            messagebox.showerror("Error", "You can't delete Path square, use 'Reset Path' instead")

        else:
            self.canvas.delete(self.filled_squares[str(SquareX)+","+str(SquareY)])
            self.np_grid[SquareY, SquareX] = 0
            del self.filled_squares[str(SquareX)+","+str(SquareY)]

    
    def chose_start_stop(self):
        if len(np.where( self.np_grid == 3)[0]) > 0 and self.current_color != 3:
            new = messagebox.askyesno("Reset", "New Start and Stop Position?")
            if new:
                squares_to_del = np.where( (self.np_grid == 2) | (self.np_grid == 3) | (self.np_grid == 4) | (self.np_grid == 5))
                self.np_grid[squares_to_del] = 0
                for y,x in zip(squares_to_del[0], squares_to_del[1]):
                    self.canvas.delete(self.filled_squares[str(x)+","+str(y)])
                    del self.filled_squares[str(x)+","+str(y)]

                self.current_color += 1
        else:
            if not (len(np.where( self.np_grid == 2)[0]) == 0 and self.current_color == 2):
                self.current_color += 1
            if self.current_color > 3:
                self.current_color = 1
        
        self.update_after_event("StartStop")


    def remove_squares(self):
        if self.removing:
            self.removing = False
        else:
            self.removing = True
        self.update_after_event("Remove"+str(int(self.removing)))


    def clear_grid(self):
        check = messagebox.askyesno("Reset Canvas", "Are Your Sure? \nThis will Clear the Entire Grid")
        if check:
            for square in self.filled_squares.values():
                self.canvas.delete(square)
            self.np_grid[np.where(self.np_grid != 0)] = 0
            self.filled_squares = {}

        self.update_after_event("Grid Cleared")


    def visualize_path_algorithm(self):
        if len(np.where( self.np_grid == 3 )[0]) == 0:
            messagebox.showwarning("Missing", "Need a Start and Stop Square to Find Path")

        else:
            start = str(np.where(self.np_grid==2)[0][0])+","+str(np.where(self.np_grid==2)[1][0])   #Dumb, fix
            end = str(np.where(self.np_grid==3)[0][0])+","+str(np.where(self.np_grid==3)[1][0])
            
            path = top_menu.radio_functions["Path Finding Algorithms"][self.current_path_algorithm.get()](self.np_grid, start, end, self)

            if not path:
                messagebox.showerror("No Path", "No Possible Path from Start to End")

            else:
                self.current_color = 4
                for square in path:
                    self.canvas.delete(self.filled_squares[square.split(",")[1]+","+square.split(",")[0]])
                    self.np_grid[int(square.split(",")[0]), int(square.split(",")[1])] = 0
                    del self.filled_squares[square.split(",")[1]+","+square.split(",")[0]]

                    self.fill_square(int(square.split(",")[1]), int(square.split(",")[0]))
                    sleep(0.03)
                    self.canvas.update_idletasks()
    
            self.current_color = 1

            self.update_after_event("Path Shown")


    def remove_found_path(self):

        for SquareY, SquareX in zip(np.where( (self.np_grid == 4) | (self.np_grid == 5) )[0], np.where( (self.np_grid == 4) | (self.np_grid == 5) )[1]):
            self.canvas.delete(self.filled_squares[str(SquareX)+","+str(SquareY)])
            self.np_grid[SquareY, SquareX] = 0
            del self.filled_squares[str(SquareX)+","+str(SquareY)]

        self.update_after_event("Path Removed")


    def display_maze(self):
        if len(np.where(self.np_grid==0)[0]) != len(self.np_grid[0]) * len(self.np_grid):
            self.clear_grid()

        if not len(np.where(self.np_grid==0)[0]) != len(self.np_grid[0]) * len(self.np_grid):
            maze_order = top_menu.radio_functions["Random Maze Algorithms"][self.current_maze_algorithm.get()](np.zeros(self.canvas_squares))

            self.current_color = 1
            min_value = 1
            max_value = np.amax(maze_order)

            while min_value <= max_value:
                squares = np.where(maze_order==min_value)
                speed = 0
                for y,x in zip(squares[0],squares[1]):
                    self.fill_square(x, y)
                    if speed%ceil((self.speed_slidebar.get()+1)/20)==0:
                        self.canvas.update_idletasks()
                        sleep(0.02)
                    speed += 1
                self.canvas.update_idletasks()
                min_value += 1

            if self.current_maze_algorithm.get() == 0:  #recursive division
                fix_maze_bug(self)


    def resize_grid(self, value):
        self.square_side = (20-int(value))*3+13
        squares_x = int((self.canvas_width-self.grid_ind*2) / self.square_side)
        squares_y = int((self.canvas_height-self.grid_ind*2) / self.square_side)
        self.canvas_squares = (squares_y, squares_x)

        for line in self.grid_lines:
            self.canvas.delete(line)
            del line

        self.create_grid()
        if len(self.filled_squares) > 0:
            old_np_grid = np.copy(self.np_grid)
        self.np_grid = np.zeros(self.canvas_squares)
        coords_to_del = []
        squares_to_remove = ([],[])
        for coord in self.filled_squares.keys():
            sq_x, sq_y = int(coord.split(",")[0]), int(coord.split(",")[1])
            self.canvas.delete(self.filled_squares[coord])
            try:
                self.np_grid[sq_y, sq_x] = old_np_grid[sq_y, sq_x]
                self.current_color = int(old_np_grid[sq_y, sq_x])
                self.fill_square(sq_x, sq_y)
            except IndexError:
                coords_to_del.append(coord)
                if old_np_grid[sq_y, sq_x] == 2 or old_np_grid[sq_y, sq_x] == 3:
                    squares_to_remove = np.where((old_np_grid==2) | (old_np_grid==3) | (old_np_grid==4) | (old_np_grid==5))


        for y,x in zip(squares_to_remove[0], squares_to_remove[1]):
            try:
                self.np_grid[y,x] = 1
                self.remove_square(x,y)
            except IndexError:
                pass


        self.current_color = 1

        for coord_to_del in coords_to_del:
            del self.filled_squares[coord_to_del]


    def update_after_event(self, event):
        if event == "StartStop":
            top_menu.update_menu(event)
            self.removing = False

        elif event == "Remove0":
            self.canvas.config(cursor="arrow")
            top_menu.update_menu(event)
        
        elif event == "Remove1":
            self.canvas.config(cursor="tcross")
            top_menu.update_menu(event)

        elif event == "Grid Cleared":
            self.removing = False
            root.config(cursor="arrow")
            top_menu.update_menu(event)

        elif event == "Path Shown":
            top_menu.update_menu(event)

        elif event == "Path Removed":
            top_menu.update_menu(event)


             
class Menu_bar():

    def __init__(self, buttons=None, cascades=None, cascade_buttons=None, cascade_radios=None):
        self.menu = tk.Menu(root, tearoff=0)

        self.cascades = {}
        self.radio_functions = {}
        if buttons:
            self.add_buttons(buttons)
        if cascades:
            for cascade in cascades:
                self.make_cascade(cascade)
                if cascade_buttons:
                    for name, attribute in cascade_buttons[cascade]:
                        self.add_to_cascade(cascade, name, attribute, "button")
                elif cascade_radios:
                    for name, attribute in cascade_radios[cascade]:
                        self.add_to_cascade(cascade, name, attribute, "radio")


    def add_buttons(self, buttons):
        for name, command in buttons:
            self.menu.add_command(label=name, command=command)

    def make_cascade(self, label):
        self.cascades[label] = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(menu=self.cascades[label], label=label)

    def add_to_cascade(self, cascade_label, label, attribute, type):
        if type == "button":
            self.cascades[cascade_label].add_command(label=label, command=attribute)
        elif type == "radio":
            if cascade_label not in self.radio_functions:
                self.radio_functions[cascade_label] = []
            self.cascades[cascade_label].add_radiobutton(label=label, variable=attribute[0], value=len(self.radio_functions[cascade_label]))
            self.radio_functions[cascade_label].append(attribute[1])
          

    def update_menu(self, event):
        if event == "StartStop":
            self.menu.entryconfig(1, label="Visualize Pathfinding!")
            self.menu.entryconfig(1, command=grid.visualize_path_algorithm)

        elif event == "Remove0":
            self.menu.entryconfig(2, label="Start Erasing Squares") 
            
        elif event == "Remove1":
            self.menu.entryconfig(2, label="Stop Erasing Squares") 
            
        elif event == "Grid Cleared":
            self.menu.entryconfig(2, label="Start Erasing Squares") 
            self.menu.entryconfig(1, label="Visualize Pathfinding!")
            self.menu.entryconfig(1, command=grid.visualize_path_algorithm)   

        elif event == "Path Shown":
            self.menu.entryconfig(1, command=grid.remove_found_path)
            self.menu.entryconfig(1, label="Reset Found Path")

        elif event == "Path Removed":
            self.menu.entryconfig(1, command=grid.visualize_path_algorithm)
            self.menu.entryconfig(1, label="Visualize Pathfinding!") 
            
            
root = tk.Tk()

box1 = Frame(root)
box1.pack(fill=X)

box2 = Frame(root)
box2.pack(fill=X)

grid = Grid(1200, 850, 50, ["black", "blue", "red", "green", "gray"])


Label(box1, text="Grid Size", width=20).pack(side="left")
grid.size_slidebar.pack(fill=X)
Label(box2, text="Path Algorithm Speed", width=20).pack(side="left")
grid.speed_slidebar.pack(fill=X)

grid.canvas.pack(side="top")

top_menu = Menu_bar(buttons = [("Place Start and Stop", grid.chose_start_stop),
                               ("Visualize Pathfinding!", grid.visualize_path_algorithm),
                               ("Start Erasing Squares", grid.remove_squares),
                               ("Clear Grid", grid.clear_grid),
                               ("Generate Maze!", grid.display_maze)], 

                    cascades = ["Path Finding Algorithms", "Random Maze Algorithms"],
                    cascade_radios= {"Path Finding Algorithms": [("Dijkstras Algorithm", (grid.current_path_algorithm, visualize_dijkstras_algorithm)),
                                                                 ("A*", (grid.current_path_algorithm, visualize_A_star)),
                                                                ("To Be Created", (grid.current_path_algorithm, grid.clear_grid))],

                                      "Random Maze Algorithms": [("Recursive Division", (grid.current_maze_algorithm, recursive_division)),
                                                                ("To Be Created", (grid.current_maze_algorithm, grid.clear_grid))]})


root.config(menu=top_menu.menu)

root.mainloop()