from time import sleep
import tkinter as tk
from math import floor, ceil
from tkinter import messagebox  #Because visualstudio error even when star import
import numpy as np
import threading, json
from tkinter import *
from maze_gen import recursive_division, fix_maze_bug, scatter
from path_algorithms import visualize_dijkstras_algorithm, visualize_A_star, visualize_Greedy


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
        self.size_slidebar = Scale(slidebar1_box, from_=0, to=20, orient=HORIZONTAL, command=self.resize_grid)
        self.size_slidebar.set(10)
        self.speed_slidebar = Scale(slidebar2_box, from_=0, to=100, orient=HORIZONTAL)
        self.speed_slidebar.set(60)
   
        self.current_path_algorithm = IntVar()
        self.current_maze_algorithm = IntVar()
        self.cancel_algorithm = False
        self.path = []
        self.squares_searched = 0
        
        self.canvas = tk.Canvas(box1, height=canvas_height, width=canvas_width, bg='white')
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
                del self.filled_squares[str(SquareX)+","+str(SquareY)]
                del self.filled_squares[str(Second_square[1][0])+","+str(Second_square[0][0])]
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


    def call_path_algorithm(self):
        if len(np.where( self.np_grid == 3 )[0]) == 0:
            messagebox.showwarning("Missing", "Need a Start and Stop Square to Find Path")

        else:
            start = str(np.where(self.np_grid==2)[0][0])+","+str(np.where(self.np_grid==2)[1][0])   #Dumb, fix
            end = str(np.where(self.np_grid==3)[0][0])+","+str(np.where(self.np_grid==3)[1][0])
            threading.Thread(target=lambda: self.visualize_path_algorithm(start,end, True)).start()
            if self.current_path_algorithm.get() > 2:
                threading.Thread(target=lambda: self.visualize_path_algorithm(end,start, False)).start()
            
            
    def visualize_path_algorithm(self, start, end, update):
        self.disable_before_algorithm()
        if self.current_path_algorithm.get() < 3:
            bidirectional = False
        else:
            bidirectional = True
        path, squares_searched = top_menu.radio_functions["Path Finding Algorithms"][self.current_path_algorithm.get()](self.np_grid, start, end, self, bidirectional, update)

        if path == False:
            messagebox.showerror("No Path", "No Possible Path from Start to End")
        else:
            if bidirectional:
                if len(self.path) > 0:
                    self.path += path
                    self.squares_searched += squares_searched
                    self.visualize_path(self.path)
                else:
                    self.path = path
                    self.squares_searched = squares_searched
            else:
                self.path = path
                self.squares_searched = squares_searched
                self.visualize_path(self.path)

            
    def visualize_path(self, path):
        self.current_color = 4
        for square in path:
            self.canvas.delete(self.filled_squares[square.split(",")[1]+","+square.split(",")[0]])
            self.np_grid[int(square.split(",")[0]), int(square.split(",")[1])] = 0
            del self.filled_squares[square.split(",")[1]+","+square.split(",")[0]]

            self.fill_square(int(square.split(",")[1]), int(square.split(",")[0]))
            sleep(0.03)
            self.canvas.update_idletasks()
        update_text((len(self.path), self.squares_searched))
        self.current_color = 1
        self.path = []
        self.squares_searched = 0
        self.update_after_event("Path Shown")
        self.enable_after_algorithm()
        self.cancel_algorithm = False


    def remove_found_path(self):
        for SquareY, SquareX in zip(np.where( (self.np_grid == 4) | (self.np_grid == 5) )[0], np.where( (self.np_grid == 4) | (self.np_grid == 5) )[1]):
            self.canvas.delete(self.filled_squares[str(SquareX)+","+str(SquareY)])
            self.np_grid[SquareY, SquareX] = 0
            del self.filled_squares[str(SquareX)+","+str(SquareY)]

        self.update_after_event("Path Removed")


    def create_maze(self):
        if len(np.where(self.np_grid==0)[0]) != len(self.np_grid[0]) * len(self.np_grid):
            self.clear_grid()

        if not len(np.where(self.np_grid==0)[0]) != len(self.np_grid[0]) * len(self.np_grid):
            maze_order = top_menu.radio_functions["Maze/Pattern Algorithms"][self.current_maze_algorithm.get()](np.zeros(self.canvas_squares))

        threading.Thread(target=lambda: self.display_maze(maze_order)).start()


    def display_maze(self, maze_order):
            self.disable_before_algorithm()
            self.current_color = 1
            min_value = 1
            max_value = np.amax(maze_order)

            while min_value <= max_value and self.cancel_algorithm==False:
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

            if self.current_maze_algorithm.get() == 0 and self.cancel_algorithm==False:  #recursive division
                fix_maze_bug(self)
            self.enable_after_algorithm()
            self.cancel_algorithm = False


    def cancel_current_algorithm(self):
        self.cancel_algorithm = True


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


    def disable_before_algorithm(self):
        self.size_slidebar.config(state=DISABLED)
        top_menu.menu.entryconfig(1, state=DISABLED)
        top_menu.menu.entryconfig(4, state=DISABLED)
        top_menu.menu.entryconfig(0, state=DISABLED)
        self.canvas.bind("<Button>", lambda event:None)
        self.canvas.bind("<B1-Motion>", lambda event:None)

        top_menu.menu.entryconfig(5, state=NORMAL)
    
    def enable_after_algorithm(self):
        self.size_slidebar.config(state=NORMAL)
        top_menu.menu.entryconfig(1, state=NORMAL)
        top_menu.menu.entryconfig(4, state=NORMAL)
        top_menu.menu.entryconfig(0, state=NORMAL)
        top_menu.menu.entryconfig(5, state=DISABLED)
        self.canvas.bind("<Button>", self.check_mouse_type)
        self.canvas.bind("<B1-Motion>", self.check_mouse_type)


    def update_after_event(self, event):
        if event == "StartStop":
            top_menu.update_menu(event)
            self.removing = False
            self.path = []
            self.squares_searched = 0
            update_text((0,0))

        elif event == "Remove0":
            self.canvas.config(cursor="arrow")
            top_menu.update_menu(event)
        
        elif event == "Remove1":
            self.canvas.config(cursor="tcross")
            top_menu.update_menu(event)

        elif event == "Grid Cleared":
            self.removing = False
            self.canvas.config(cursor="arrow")
            top_menu.update_menu(event)
            self.path = []
            self.squares_searched = 0
            update_text((0,0))

        elif event == "Path Shown":
            top_menu.update_menu(event)

        elif event == "Path Removed":
            top_menu.update_menu(event)
            self.path = []
            self.squares_searched = 0
            update_text((0,0))


             
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
            if cascade_label == "Path Finding Algorithms":
                self.cascades[cascade_label].add_radiobutton(label=label, variable=attribute[0], value=len(self.radio_functions[cascade_label]), command=update_text)
            else:
                self.cascades[cascade_label].add_radiobutton(label=label, variable=attribute[0], value=len(self.radio_functions[cascade_label]))
            self.radio_functions[cascade_label].append(attribute[1])
          

    def update_menu(self, event):
        if event == "StartStop":
            self.menu.entryconfig(1, label="Visualize Pathfinding!")
            self.menu.entryconfig(1, command=grid.call_path_algorithm)

        elif event == "Remove0":
            self.menu.entryconfig(2, label="Start Erasing Squares") 
            
        elif event == "Remove1":
            self.menu.entryconfig(2, label="Stop Erasing Squares") 
            
        elif event == "Grid Cleared":
            self.menu.entryconfig(2, label="Start Erasing Squares") 
            self.menu.entryconfig(1, label="Visualize Pathfinding!")
            self.menu.entryconfig(1, command=grid.call_path_algorithm)   

        elif event == "Path Shown":
            self.menu.entryconfig(1, command=grid.remove_found_path)
            self.menu.entryconfig(1, label="Reset Found Path")

        elif event == "Path Removed":
            self.menu.entryconfig(1, command=grid.call_path_algorithm)
            self.menu.entryconfig(1, label="Visualize Pathfinding!") 
            

def update_text(data=None):
    if data == None:
        current_algorithm.config(text=algorithm_data[grid.current_path_algorithm.get()]["name"])
        algorithm_description.config(text=algorithm_data[grid.current_path_algorithm.get()]["description"])
    else:
        path_lengh_label.config(text="\n\n\n\nPath's Length Measured in Squares: \n"+str(data[0]))
        squares_searched_label.config(text="\n Total Squares Searched: \n"+str(data[1]))
        

root = tk.Tk()

slidebar1_box = Frame(root)
slidebar1_box.pack(fill=X)

slidebar2_box = Frame(root)
slidebar2_box.pack(fill=X)

rest = Frame(root)
rest.pack(side="top", fill=BOTH)

box1 = Frame(rest)
box1.grid(row=0,column=0, sticky="nswe")
box2 = Frame(rest)
box2.grid(row=0,column=1, sticky="nswe")
rest.columnconfigure(0, weight=2)
rest.columnconfigure(1, weight=1)

grid = Grid(1200, 850, 50, ["black", "blue", "red", "green", "gray"])

Label(slidebar1_box, text="Grid Size", width=20).pack(side="left")
grid.size_slidebar.pack(fill=X)
Label(slidebar2_box, text="Algorithm Speed", width=20).pack(side="left")
grid.speed_slidebar.pack(fill=X)

grid.canvas.pack(side="right")

subbox1 = Frame(box2)
subbox2 = Frame(box2)
subbox3 = Frame(box2)
subbox1.grid(row=0, column=0, sticky="nswe")
subbox2.grid(row=1, column=0, sticky="nswe")
subbox3.grid(row=2, column=0, sticky="nswe")
box2.rowconfigure(0,weight=1)
box2.rowconfigure(1,weight=1)
box2.rowconfigure(2,weight=1)
box2.columnconfigure(0, weight=1)

top_menu = Menu_bar(buttons = [("Place Start and Stop", grid.chose_start_stop),
                               ("Visualize Pathfinding!", grid.call_path_algorithm),
                               ("Start Erasing Squares", grid.remove_squares),
                               ("Clear Grid", grid.clear_grid),
                               ("Generate Maze/Pattern!", grid.create_maze),
                               ("Cancel Algorithm", grid.cancel_current_algorithm)],

                    cascades = ["Path Finding Algorithms", "Maze/Pattern Algorithms"],
                    cascade_radios= {"Path Finding Algorithms": [("Dijkstra's Algorithm", (grid.current_path_algorithm, visualize_dijkstras_algorithm)),
                                                                 ("A*", (grid.current_path_algorithm, visualize_A_star)),
                                                                 ("Greedy", (grid.current_path_algorithm, visualize_Greedy)),
                                                                 ("Bidirectional Dijkstra's", (grid.current_path_algorithm, visualize_dijkstras_algorithm)),
                                                                 ("Bidirectional A*", (grid.current_path_algorithm, visualize_A_star))],

                                      "Maze/Pattern Algorithms": [("Recursive Division", (grid.current_maze_algorithm, recursive_division)),
                                                                  ("Scatter", (grid.current_maze_algorithm, scatter)),
                                                                  ("To Be Created", (grid.current_maze_algorithm, grid.clear_grid))]})

with open("algorithm_descriptions.json", "r") as f: 
    algorithm_data = json.load(f)
current_algorithm = Label(subbox1, text=algorithm_data[grid.current_path_algorithm.get()]["name"], font=("Arial", 16))
current_algorithm.pack(side="bottom", fill=X)
algorithm_description = Label(subbox2, text=algorithm_data[grid.current_path_algorithm.get()]["description"], font=("Arial", 12))
algorithm_description.pack(side="top", fill=BOTH)

path_lengh_label = Label(subbox2, text="\n\n\n\nPath's Length Measured in Squares: \n0", font=("Arial", 14))
path_lengh_label.pack(side="top", fill=X)
squares_searched_label = Label(subbox2, text="\n Total Squares Searched: \n0", font=("Arial", 14))
squares_searched_label.pack(side="top", fill=X)

Label(subbox3, text="                                          ", font=("Arial",20)).pack(side="top")   #idk

top_menu.menu.entryconfig(5, state=DISABLED)
root.config(menu=top_menu.menu)

root.mainloop()