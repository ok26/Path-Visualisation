from time import sleep
import tkinter as tk
from math import floor, ceil
from tokenize import String
import numpy as np
from tkinter import messagebox, Label, StringVar
from maze_gen import recursive_division, fix_rec_div_bug
from path_algoritms import dijkstras_algoritm


class Grid():

    def __init__(self, square_side, canvas_width, canvas_height, grid_ind, colors):
        self.square_side = square_side
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.grid_ind = grid_ind
        self.colors = colors
        self.current_color = 1
        self.removing = False
        self.filled_squares = {}
        self.canvas_squares = (int((canvas_height-2*grid_ind)/25),int((canvas_width-2*grid_ind)/25))
        self.np_grid = np.zeros(self.canvas_squares)
        self.canvas = tk.Canvas(root, height=canvas_height, width=canvas_width, bg='white')
        self.canvas.bind("<Configure>", self.create_grid)
        self.canvas.bind("<Button>", self.check_mouse_type)
        self.canvas.bind("<B1-Motion>", self.check_mouse_type)
    

    def check_mouse_type(self, event):
        if event.num == 1:
            self.check_square(event)
        elif event.num == 3:
            pass
        elif event.num not in [1,2,3,4,5]:
            self.check_square(event)
        
        
    def create_grid(self, event):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
    
        for i in range(self.grid_ind, w-self.grid_ind, self.square_side):
            self.canvas.create_line([(i, self.grid_ind), (i, h-(h%self.square_side)-self.grid_ind)], tag='grid_line')

        for i in range(self.grid_ind, h-self.grid_ind, self.square_side):
            self.canvas.create_line([(self.grid_ind, i), (w-(w%self.square_side)-self.grid_ind, i)], tag='grid_line')

    
    def check_square(self, event):
        x = event.x
        y = event.y

        if not (x <= self.grid_ind or x >= (self.canvas_width - self.grid_ind) or y <= self.grid_ind or y >= (self.canvas_height - self.grid_ind)):

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
        check = messagebox.askyesno("Reset Canvas", "Are Your Sure? \n This will Clear the Entire Grid")
        if check:
            for square in self.filled_squares.values():
                self.canvas.delete(square)
            self.np_grid[np.where(self.np_grid != 0)] = 0
            self.filled_squares = {}

        self.update_after_event("Grid_Cleared")


    def display_shortest_path(self):
        if len(np.where( self.np_grid == 3 )[0]) == 0:
            messagebox.showwarning("Missing", "Need a Start and Stop Square to Find Path")

        else:
            start = str(np.where(self.np_grid==2)[0][0])+","+str(np.where(self.np_grid==2)[1][0])
            end = str(np.where(self.np_grid==3)[0][0])+","+str(np.where(self.np_grid==3)[1][0])

            tentatives, path = dijkstras_algoritm(self.np_grid, start, end)
            smallest_tent = 0
            self.current_color = 5
            while True:
                squares_to_show = [k for k,v in tentatives.items() if v == smallest_tent+1]
                if smallest_tent >= tentatives[end] or len(squares_to_show) == 0:
                    break
                else:
                    for square in squares_to_show:
                        if square != end:
                            self.fill_square(int(square.split(",")[1]), int(square.split(",")[0]))
                    self.canvas.update_idletasks()
                    sleep(0.1)
                    smallest_tent += 1

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

        self.update_after_event("Path_Shown")


    def remove_found_path(self):

        for SquareY, SquareX in zip(np.where( (self.np_grid == 4) | (self.np_grid == 5) )[0], np.where( (self.np_grid == 4) | (self.np_grid == 5) )[1]):
            self.canvas.delete(self.filled_squares[str(SquareX)+","+str(SquareY)])
            self.np_grid[SquareY, SquareX] = 0
            del self.filled_squares[str(SquareX)+","+str(SquareY)]

        self.update_after_event("Path_Removed")


    def display_maze(self):
        if len(np.where(self.np_grid==0)[0]) != len(self.np_grid[0]) * len(self.np_grid):
            self.clear_grid()
           
        maze = recursive_division(np.zeros(self.canvas_squares))
        maze = fix_rec_div_bug(maze)
        self.current_color = 1

        squares = np.where(maze==1)
        largest_y = None
        for y,x in zip(squares[0],squares[1]):
            if largest_y == None or y > largest_y:
                self.canvas.update_idletasks()
                largest_y = y
                sleep(0.05)
            self.fill_square(x, y)


    def update_after_event(self, event):
        if event == "StartStop":
            top_menu.update_menu(event)
            self.removing = False

        elif event == "Remove0":
            self.canvas.config(cursor="arrow")
        
        elif event == "Remove1":
            self.canvas.config(cursor="tcross")

        elif event == "Clear_grid":
            self.removing = False
            root.config(cursor="arrow")
            top_menu.update_menu(event)


             
class Menu_bar():

    def __init__(self, buttons=None, cascades=None, cascade_buttons=None):
        self.menu = tk.Menu(root, tearoff=0)
        self.cascades = {}
        if buttons:
            self.add_buttons(buttons)
        if cascades:
            for cascade in cascades:
                self.make_cascade(cascade)
                for name, command in cascade_buttons[cascade]:
                    self.add_to_cascade(cascade, name, command)


    def add_buttons(self, buttons):
        for name, command in buttons:
            self.menu.add_command(label=name, command=command)

    def make_cascade(self, label):
        self.cascades[label] = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(menu=self.cascades[label], label=label)

    def add_to_cascade(self, cascade_label, label, command):
        self.cascades[cascade_label].add_command(label=label, command=command)

    def update_menu(self, event):
        pass


#start_stop: self.menu.entryconfig(3, label="Find Path", command=self.display_shortest_path)

#Start Removing: Obvious

#Clear Grid self.removing = False
            #self.menu.entryconfig(1, label="Remove Squares")
            #root.config(cursor="arrow")
            #self.menu.entryconfig(3, label="Find Path", command=self.display_shortest_path)

#Find Path self.menu.entryconfig(3, label="Reset Path", command=self.remove_found_path)

#Remove found path: self.menu.entryconfig(3, label="Find Path", command=self.display_shortest_path) 




root = tk.Tk()

grid = Grid(25, 1200, 800, 50, ["black", "blue", "red", "green", "gray"])
grid.canvas.pack(side="bottom")

top_menu = Menu_bar(buttons = [("Place Start and Stop", grid.chose_start_stop),
                               ("Start Removing Squares", grid.remove_squares),
                               ("Clear Grid", grid.clear_grid)], 

                    cascades = ["Path Finding Algoritms", "Random Maze Algoritms"],
                    cascade_buttons={"Path Finding Algoritms": [("Dijkstrs Algoritm", grid.display_shortest_path),
                                                                ("To Be Created", grid.clear_grid)],

                                      "Random Maze Algoritms": [("Recursive Division", grid.display_maze),
                                                                ("To Be Created", grid.clear_grid)]})


root.config(menu=top_menu.menu)

root.mainloop()