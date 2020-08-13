### A* Pathfinding Algorithm Visualizer
# https://en.wikipedia.org/wiki/A*_search_algorithm

import pygame
import math
from queue import PriorityQueue

SIZE = 800 #Window is going to be a square so we only need one variable for both Length and Width
WIN = pygame.display.set_mode((SIZE, SIZE)) #Setting Window Size
pygame.display.set_caption("A* Pathfinding Algorithm Visualizer") #Window Title

#Defining RGB Color Codes for our Cells
#THe Color of the cell will let us know what kind of cell/what attributes a cell has
BLACK = (0 , 0, 0) #Barrier
WHITE = (255, 255, 255) #Empty
GRAY = (128, 128, 128)
RED = (255, 0 , 0) #Closed
GREEN = (0, 255, 0) #Open
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0) #Start
PURPLE = (128, 0 , 128) #End
TURQUOISE = (64, 224, 208) #Path

class Cell:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows

    #Gets the position of the cell
    def get_pos(self):
        return self.row, self.col
    
    #Methods that check the type of cell
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    #Methods that set/make cells 
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE
    
    def make_path(self):
        self.color = TURQUOISE

    #Resets cell back to empty/white
    def reset(self):
        self.color = WHITE

    #Draws Cell
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    #Checks and updates neighboring Cells
    def update_neighbors(self, grid):
        self.neighbors = []

        #DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        #UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        #RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        #LEFT
        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

#Defining our heuristic to calculate the distance between two points (p1 and p2)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#Reconstructs shortest path between start and end to draw
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

#Algorithm Logic
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        #Allows user to quit program while algorithm is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        #Makes path if current cell is the end cell
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False        

#Makes grid of cells
def make_grid(rows, size):
    grid = []
    gap = size // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i , j, gap, rows)
            grid[i].append(cell)

    return grid

#Draws the grid lines onto the Window
def draw_grid(win, rows, size):
    gap = size // rows
    #For loop draws vertical lines
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (size, i * gap))
        #Draws horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, size))

def draw(win, grid, rows, size):
    win.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw(win)
    
    draw_grid(win, rows, size)
    pygame.display.update()

def get_clicked_pos(pos, rows, size):
    gap = size // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

#MAIN LOOP
def main(win, size):
    ROWS = 50
    grid = make_grid(ROWS, size)

    #Start/End Cells
    start_cell = None
    end_cell = None

    run = True

    #Main loop
    while run:
        draw(win, grid, ROWS, size)
        #Checks for different types of events that may happen
        for event in pygame.event.get():
            #Quit Event
            if event.type == pygame.QUIT:
                run = False

            #Left Mouse Click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, size)
                cell = grid[row][col]

                #If Start cell does not exist, make it
                if not start_cell and cell != end_cell:
                    start_cell = cell
                    start_cell.make_start()

                #If End cell does not exist, make it
                elif not end_cell and cell != start_cell:
                    end_cell = cell
                    end_cell.make_end()

                #make barrier cells
                elif cell != end_cell and cell != start_cell:
                    cell.make_barrier()

            #Right Mouse Click/Erase
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, size)
                cell = grid[row][col]
                cell.reset()

                if cell == start_cell:
                    start_cell = None
                elif cell == end_cell:
                    end_cell = None

            #SPACEBAR starts the pathfinding algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_cell and end_cell:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, size), grid, start_cell, end_cell)

    pygame.quit()
main(WIN, SIZE)