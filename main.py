import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style

import heapq
import time
import numpy as np
from random import randrange
from random import choice

from collections import deque

import tkinter as tk

def a_star(maze):
    global order
    size = len(maze)

    line, col = 1, 1
    parent = {(line, col): None}
    pq = [(0, (line, col))]

    order = deque()
    order.append((line, col))

    manhattan_distance = [[(abs(line-size+2) + abs(col-size+2)) for line in range(size)] for col in range(size)]

    while pq:
        cur = heapq.heappop(pq)
        d, line, col = cur[0], cur[1][0], cur[1][1]

        order.append((line, col))

        if (line, col) != (1, 1):
            d -= manhattan_distance[parent[(line, col)][0]][parent[(line, col)][1]] #Garde seulement la distance réelle

        d = d+manhattan_distance[line][col]
        if (line, col) == (size-2, size-2):
            ans = [(size - 2, size - 2), (size-2, size-1)]
            while parent[(line, col)]:
                ans.insert(0, parent[(line, col)])
                line, col = parent[(line, col)]
            ans.insert(0, (1, 0))
            return ans

        adj_cases = [(line + 1, col), (line - 1, col), (line, col + 1), (line, col - 1)]
        for case in adj_cases:
            adj_line, adj_col = case[0], case[1]
            if (adj_line, adj_col) not in parent.keys() and maze[adj_line][adj_col] != 1:
                parent[(adj_line, adj_col)] = (line, col)
                heapq.heappush(pq, (d+1, (adj_line, adj_col)))


def dijkstra(maze):
    global order

    size = len(maze)

    line, col = 1, 1
    parent = {(line, col): None}
    distance = {(line, col): 0}
    pq = [(0, (line, col))]

    order = deque()
    order.append((line, col))

    while pq:
        cur = heapq.heappop(pq)
        d, line, col = cur[0], cur[1][0], cur[1][1]

        order.append((line, col))

        if (line, col) == (size-2, size-2):
            ans = [(size - 2, size - 2), (size-2, size-1)]
            while parent[(line, col)]:
                ans.insert(0, parent[(line, col)])
                line, col = parent[(line, col)]
            ans.insert(0, (1, 0))
            return ans

        adj_cases = [(line + 1, col), (line - 1, col), (line, col + 1), (line, col - 1)]
        for case in adj_cases:
            adj_line, adj_col = case[0], case[1]
            if ((adj_line, adj_col) not in distance.keys() or d+1 < distance[(adj_line, adj_col)]) \
                    and maze[adj_line][adj_col] != 1:
                parent[(adj_line, adj_col)] = (line, col)
                distance[(adj_line, adj_col)] = d+1
                heapq.heappush(pq, (d+1, (adj_line, adj_col)))

def DFS_search(maze):
    """Fonction qui renvoie le chemin pour aller du début à la fin en liste par DFS"""
    global levels
    def DFS_visit(line, col, maze, parent, size, level):
        nonlocal path
        if len(path) == 0:
            if (line, col) == (size - 2, size - 2):
                ans = [(size - 2, size - 2), (size - 2, size - 1)]
                while parent[(line, col)]:
                    ans.insert(0, parent[(line, col)])
                    line, col = parent[(line, col)]
                path = ans
                ans.insert(0, (1, 0))
                return

            adj_cases = [(line + 1, col), (line - 1, col), (line, col + 1), (line, col - 1)]
            for case in adj_cases:
                adj_line, adj_col = case[0], case[1]

                if (adj_line, adj_col) not in parent.keys() and maze[adj_line][adj_col] != 1:  # Non opti, à faire avec le niveau d'avant seulement(avec une liste)
                    parent[(adj_line, adj_col)] = (line, col)
                    levels[(adj_line, adj_col)] = level

                    DFS_visit(adj_line, adj_col, maze, parent, size, level+1)


    size = len(maze)

    line, col = 1, 1
    parent = {(line, col): None}
    levels = {(line, col): 0}

    path = []
    DFS_visit(line, col, maze, parent, size, 1)

    return path

def BFS_search(maze):
    """Fonction qui envoie le chemin pour aller du début à la fin ?"""
    global size, levels

    size = len(maze)

    line, col = 1, 1

    levels = {(line, col): 0}
    parent = {(line, col): None}
    frontier = [(line, col)]
    i = 1
    while frontier: #Cas trop général, à améliorer
        next_search = []
        for line, col in frontier:
            adj_cases = [(line+1, col), (line-1, col), (line, col+1), (line, col-1)]
            for case in adj_cases:
                adj_line, adj_col = case[0], case[1]
                if (adj_line, adj_col) not in levels.keys() and maze[adj_line][adj_col] != 1: #Non opti, à faire avec le niveau d'avant seulement(avec une liste)
                    levels[(adj_line, adj_col)] = i
                    parent[(adj_line, adj_col)] = (line, col)

                    if (adj_line, adj_col) == (size-2, size-2):
                        ans = [(size - 2, size - 2), (size - 2, size - 1)]
                        while parent[(adj_line, adj_col)]:
                            ans.insert(0, parent[(adj_line, adj_col)])
                            adj_line, adj_col = parent[(adj_line, adj_col)]
                        ans.insert(0, (1, 0))
                        return ans

                    next_search.append((adj_line, adj_col))
        frontier = next_search
        i += 1



def solver(input):
    global path, maze, phase, method, size, again, maze_1

    if not again:
        maze_1 = [row[:] for row in maze]
    if again:
        maze = [row[:] for row in maze_1]

    if input == 1:
        method = a_star
    elif input == 2:
        method = dijkstra
    elif input ==3:
        method = DFS_search
    elif input == 4:
        method = BFS_search
    else:
        print("Invalid input")
        method = DFS_search

    path = method(maze)

    phase = 6


def animate_pathfinding(frames):
    global phase, method, maze, img, ax_2, order, again
    if phase == 6:
        maze = clean(maze)
        img = ax_2.imshow(maze, interpolation='none', vmin=0, vmax=255, cmap="nipy_spectral")

        if method == BFS_search or method == DFS_search:
            order = deque(levels.keys())

        order.appendleft((1, 0))
        order.append((len(maze)-2, len(maze)-1))

        phase = 7

    if phase == 7:
        if order:
            item = order.popleft()

            maze[item[0]][item[1]] = (100, 0, 0)
            img.set_data(maze)

        else:
            again = 1
            clean(maze, again)
            img = ax_2.imshow(maze, interpolation='none', vmin=0, vmax=255, cmap="nipy_spectral")
            phase = 8


def is_finished(maze, size):
    for i in range(1, size, 2):
        for j in range(1, size, 2):
            if maze[i][j] != maze[1][1]:
                return False
    return True


def explore(line, col, number):
    if maze[line + 1][col] != number and maze[line + 1][col] != 1:
        maze[line + 1][col] = number
        explore(line + 1, col, number)

    if maze[line - 1][col] != number and maze[line - 1][col] != 1:
        maze[line - 1][col] = number
        explore(line - 1, col, number)

    if maze[line][col + 1] != number and maze[line][col + 1] != 1:
        maze[line][col + 1] = number
        explore(line, col + 1, number)

    if maze[line][col - 1] != number and maze[line][col - 1] != 1:
        maze[line][col - 1] = number
        explore(line, col - 1, number)


def animate(i):
    """Algorithme de fusion aléatoire de chemins pour générer un labyrinthe."""
    global maze, phase, walls, numbers, size, difficulty, img, fig, ax, nb

    if phase == 1:
        size = size * 2 + 1

        a = 10
        # ======= Creates the grid of 1 and a, 1 is a wall and a is a hole =======
        maze = [[1 for i in range(size)] for j in range(size)]  # Create a full square of 1
        for line in range(1, size, 2):
            for col in range(1, size, 2):  # Create the blanks of 2 in the grid
                maze[line][col] = a
                a += 255 / (size // 2) ** 2

        # ====== Creates the list of all the walls of the maze ========
        walls = []
        for line in range(1, size, 2):
            for col in range(2, size - 1, 2):
                walls.append((line, col))

        for line in range(2, size - 1, 2):
            for col in range(1, size, 2):
                walls.append((line, col))

        numbers = []
        img = ax.imshow(maze, interpolation='none', vmin=0, vmax=255, cmap="nipy_spectral")
        phase += 1

    if phase == 2:
        # ====== Choose one wall randomly each time and harmonizes ====
        if not is_finished(maze, size):  # Tant que le labyrinthe est pas "harmonisé"
            wall = walls.pop(randrange(len(walls)))  # Choisit un mur aléatoirement

            if not wall[0] % 2 == 0:  # Si le mur est pas sur une ligne pleine donc mur gauche/droite
                left_nb = maze[wall[0]][wall[1] - 1]
                right_nb = maze[wall[0]][wall[1] + 1]

                if left_nb != right_nb:  # Pour avoir labyrinthe simple
                    if left_nb in numbers:  # On optimise pour répandre le chiffre le + présent
                        number = left_nb
                    elif right_nb in numbers:
                        number = right_nb
                    else:
                        number = choice([left_nb, right_nb])
                        numbers.append(number)

                    maze[wall[0]][wall[1]] = number
                    explore(wall[0], wall[1], number)  # On explore les chiffres pour les changer

            else:  # Si mur sur ligne plein donc mur haut/bas
                left_nb = maze[wall[0] - 1][wall[1]]
                right_nb = maze[wall[0] + 1][wall[1]]

                if left_nb != right_nb:  # Pour avoir labyrinthe simple
                    if left_nb in numbers:  # On optimise pour prendre un chiffre déjà répandu, donc limiter explore
                        number = left_nb
                    elif right_nb in numbers:
                        number = right_nb
                    else:
                        number = choice([left_nb, right_nb])
                        numbers.append(number)

                    maze[wall[0]][wall[1]] = number
                    explore(wall[0], wall[1], number)

            img.set_data(maze)
        else:
            phase += 1
            nb = maze[1][1]

    if phase == 3:
        # ====== Create a complex labyrinth ========
        maze[1][0] = nb
        maze[size-2][size-1] = nb
        img.set_data(maze)
        if difficulty:
            for i in range(difficulty):  # Plus la difficulté est élevée, plus on casse de blocs.
                if len(walls):
                    wall = walls.pop(randrange(len(walls)))  # Choisit un mur aléatoirement et le casse
                    maze[wall[0]][wall[1]] = nb
                    img.set_data(maze)
        else:
            phase += 1

    if phase == 4:
        # ====== Clean les valeurs pour l'affichage ========
        nb = maze[1][1]
        for i in range(size):
            for j in range(size):
                if maze[i][j] == nb:
                    maze[i][j] = 0

        phase += 1


def afficher(frames):
    global maze, path, img, phase, turn

    if phase == 8:
        if turn < len(path)-1:
            i = turn
            a = path[i]
            b = path[i + 1]

            # Blue - red
            r = int((i / len(path)) * 255)
            px = (r, 0, 255 - r)

            if a[0] == b[0]:
                # horizontal line
                for col in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                    maze[a[0]][col] = px
            elif a[1] == b[1]:
                # vertical line
                for line in range(min(a[0], b[0]), max(a[0], b[0])):
                    maze[line][a[1]] = px

            img.set_data(maze)
            turn += 1



def clean(maze, again=0):
    # ==== Clean the maze for matplotlib =======
    size = len(maze)
    if not again:
        for i in range(size):
            for j in range(size):
                if maze[i][j] == 1:
                    maze[i][j] = (0, 0, 0)
                else:
                    maze[i][j] = (255, 255, 255)

        maze[1][0] = (255, 255, 255)
        maze[len(maze) - 2][len(maze) - 1] = (255, 255, 255)

        maze = np.array(maze, dtype=np.uint8)

    else:
        for i in range(size):
            for j in range(size):
                if maze[i][j][0] != 0:
                    maze[i][j] = (255, 255, 255)

    return maze


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Maze Solver")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (GenerateMaze, SolveMaze, ShowMaze, ShowPath):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_next(GenerateMaze)

    def show_next(self, context, *args):
        global size, difficulty, phase, turn, ani, again
        frame = self.frames[context]
        frame.tkraise()
        if context == ShowMaze:
            size, difficulty = args[0], args[1]
            if not (1 <= size <= 40) or difficulty < 0:
                self.show_next(GenerateMaze)
                return
            phase = 1

        if context == ShowPath:
            solver(args[0])
            phase = 6
            turn = 0

        if context == GenerateMaze:
            again = 0



class GenerateMaze(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg="#506980")

        label_1 = tk.Label(self, text="The size you want for the maze, an int between 1 and 40:", bg="#B37E25",
                           font=("Verdana", 14), fg="white")
        size = tk.Entry(self, width=3, bg="#F8F8FC", fg="black", font=("Verdana", 14))
        label_2 = tk.Label(self, text="The difficulty for a complex maze(int), 0 if not complex:", bg="#B37E25",
                           font=("Verdana", 14), fg="white")
        difficulty = tk.Entry(self, width=3, bg="#F8F8FC", fg="black", font=("Verdana", 14))
        # size.insert(0, "Put the size you want for your maze, 1-50.")
        # difficulty.insert(0, "Put the difficulty you want for a complex maze, 0 if you want a maze with one path.")
        button_1 = tk.Button(self, text="Generate a maze",
                             command=lambda: controller.show_next(ShowMaze, int(size.get()), int(difficulty.get())), bg="#A1D3FF",
                             fg="white", font=("Segoe UI Black", 18),
                             padx=40, pady=40)
        label_1.grid(row=0, column=0, padx=50, pady=50)
        size.grid(row=0, column=1, padx=70)
        label_2.grid(row=1, column=0, padx=50, pady=50)
        difficulty.grid(row=1, column=1, padx=70)
        button_1.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=80, padx=90)


class SolveMaze(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg="#506980")

        label_1 = tk.Label(self, text="Select the pathfinding algorithm you want:\n"
                                      "- 1: A-star, doesn't gives the best path but is fast\n"
                                      "- 2: Dijkstra, looks like BFS in this case\n"
                                      "- 3: DFS, doesn't gives the best path but is fast in some cases"
                                      "\n- 4: BFS, always gives the best path but is pretty slow.", bg="#B37E25",
                           font=("Verdana", 14), fg="white", justify="left")

        algorithm = tk.Entry(self, width=3, bg="#F8F8FC", fg="black", font=("Verdana", 14))

        button_2 = tk.Button(self, text="Solve the maze", command=lambda: controller.show_next(ShowPath, int(algorithm.get())), bg="#A1D3FF",
                             fg="white", padx=10, pady=10, font=("Segoe UI Black", 18))

        label_1.pack(pady=20)
        algorithm.pack(pady=10)
        button_2.pack(pady=80, padx=90)


class ShowMaze(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(sid=tk.TOP, fill=tk.BOTH, expand=True)

        button = tk.Button(self, text="Next step", command=lambda: controller.show_next(SolveMaze), bg="#A1D3FF",
                           fg="white", font=("Segoe UI Black", 10), padx=10, pady=10)

        button.pack()


class ShowPath(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = FigureCanvasTkAgg(fig_2, self)
        canvas.draw()
        canvas.get_tk_widget().pack(sid=tk.TOP, fill=tk.BOTH, expand=True)

        button = tk.Button(self, text="Try Again", command=lambda: controller.show_next(SolveMaze), bg="#A1D3FF",
                           fg="white", font=("Segoe UI Black", 10), padx=50, pady=10)
        button.pack(pady=5)

        button = tk.Button(self, text="Generate a new maze", command=lambda: controller.show_next(GenerateMaze), bg="#DB564F",
                           fg="white", font=("Segoe UI Black", 8), padx=8, pady=8)
        button.pack(pady=5)


phase = 0
fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)
fig_2 = Figure(figsize=(5, 5), dpi=100)
ax_2 = fig_2.add_subplot(111)
again = 0

gui = GUI()
ani = animation.FuncAnimation(fig, animate, frames=100, interval=1)
ani_3 = animation.FuncAnimation(fig_2, animate_pathfinding, frames=100, interval=1)
ani_2 = animation.FuncAnimation(fig_2, afficher, frames=100, interval=1)

gui.mainloop()