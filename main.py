from numpy.random import choice
import pygame
from queue import PriorityQueue

WINDOW = (WIDTH, HEIGHT) = (402, 402)  # size of window
SQUARE = 20
COLS = WIDTH // SQUARE
ROWS = HEIGHT // SQUARE

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(WINDOW)  # pygame window
clock = pygame.time.Clock()  # tracking time


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.path = choice([False, True], p=[0.25, 0.75])
        self.start = False
        self.end = False
        self.neighbors = []
        self.in_queue = False  # if true, node is in priority queue
        self.out_queue = False  # if true, node is not in priority queue
        self.shortest_path = False

    def draw(self, screen):
        x = self.row * SQUARE
        y = self.col * SQUARE

        if self.path:
            pygame.draw.rect(screen, pygame.Color('white'), (x, y, SQUARE, SQUARE))

        if self.start:
            pygame.draw.rect(screen, pygame.Color('chartreuse1'), (x, y, SQUARE, SQUARE))

        if self.end:
            pygame.draw.rect(screen, pygame.Color('red'), (x, y, SQUARE, SQUARE))

        if self.in_queue:
            pygame.draw.rect(screen, pygame.Color('darkorchid1'), (x, y, SQUARE, SQUARE))

        if self.out_queue:
            pygame.draw.rect(screen, pygame.Color('cadetblue1'), (x, y, SQUARE, SQUARE))

        if self.shortest_path:
            pygame.draw.rect(screen, pygame.Color('gold'), (x, y, SQUARE, SQUARE))

        # drawing walls of each square in grid
        pygame.draw.line(screen, pygame.Color('black'), (x, y), (x + SQUARE, y), 2)
        pygame.draw.line(screen, pygame.Color('black'), (x + SQUARE, y), (x + SQUARE, y + SQUARE), 2)
        pygame.draw.line(screen, pygame.Color('black'), (x + SQUARE, y + SQUARE), (x, y + SQUARE), 2)
        pygame.draw.line(screen, pygame.Color('black'), (x, y + SQUARE), (x, y), 2)

    def get_row_col(self):
        return self.row, self.col

    # determines if cell is valid
    def valid_neighbor(self, col, row, grid):
        if col > COLS - 1 or col < 0 or row > ROWS - 1 or row < 0:  # check if cell is out of bounds in grid
            return False

        return grid[row][col]

    # returns neighbors of a cell
    def get_neighbors(self, grid):
        self.neighbors = []
        top = self.valid_neighbor(self.row, self.col - 1, grid)
        right = self.valid_neighbor(self.row + 1, self.col, grid)
        bottom = self.valid_neighbor(self.row, self.col + 1, grid)
        left = self.valid_neighbor(self.row - 1, self.col, grid)

        if top and top.path:
            self.neighbors.append(top)
        if right and right.path:
            self.neighbors.append(right)
        if bottom and bottom.path:
            self.neighbors.append(bottom)
        if left and left.path:
            self.neighbors.append(left)


def h(x1, y1, x2, y2):  # manhattan distance has heuristic function since we only do vertical and horizontal traversing
    return abs(x1 - x2) + abs(y1 - y2)


# using mouse position, method return which row and column coordinate the mouse has clicked on
def get_mouse_pos(pos, rows, width):
    x, y = pos
    row = y // (width // rows)
    col = x // (width // rows)
    return row, col


def backtrack_path(previous, cell, start):
    while cell in previous:  # flags the shortest path to ending cell
        cell = previous[cell]
        # if cell is start node we set shortest_path of the cell to false so that start node will have different color
        # than the shortest path
        if cell == start:
            cell.shortest_path = False
        else:
            cell.shortest_path = True


def astar(grid, start, end):
    count = 0  # in case there are two f scores are the same we use count to determine priority
    open_set = PriorityQueue()  # (f_score, count, node)
    open_set.put((0, count, start))
    previous = {}  # current_cell:previous_cell, used to backtrack to find the shortest path

    # setting all g and f scores to infinity
    g_score = {}
    for row in grid:
        for cell in row:
            g_score[cell] = float("inf")
    g_score[start] = 0

    f_score = {}
    for row in grid:
        for cell in row:
            f_score[cell] = float("inf")
    f_score[start] = h(start.row, start.col, end.row, end.col)

    # set copy of open_set, used to see whether cells are in the open_set (easier to check with using a set
    # than the priority queue because each element in priority queue is tuple)
    open_set_copy = {start}

    while not open_set.empty():
        for event in pygame.event.get():  # if the user quits while algorithm is running
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = open_set.get()[2]  # gets cell with lowest f score
        open_set_copy.remove(curr)

        if curr == end:
            backtrack_path(previous, end, start)
            # if the end is found we set open to false so that the end cell will be a different color
            curr.in_queue = False
            return True

        for neighbor in curr.neighbors:
            # note that all weights of edges are 1
            temp_g_score = g_score[curr] + 1  # adding 1 to g_score to simulate movement of curr to any adj cell
            if temp_g_score < g_score[neighbor]:
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.row, neighbor.col, end.row, end.col)
                previous[neighbor] = curr

                if neighbor not in open_set_copy:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_copy.add(neighbor)
                    neighbor.in_queue = True

        if curr != start:
            curr.out_queue = True

    return False


def main():
    start_cell = None
    end_cell = None
    is_start = False
    is_end = False

    grid = []  # 2D array containing all cells in grid

    # creating 2D list to represent grid
    for row in range(ROWS):
        grid.append([])
        for col in range(COLS):
            cell = Cell(col, row)
            grid[row].append(cell)

    while True:
        pygame.display.update()
        screen.fill(pygame.Color('deepskyblue4'))

        for row in range(ROWS):
            for col in range(COLS):
                grid[row][col].draw(screen)  # drawing all cells in grid

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if pygame.mouse.get_pressed()[0]:  # left click to set start cell
                mouse_pos = pygame.mouse.get_pos()
                r, c = get_mouse_pos(mouse_pos, ROWS, WIDTH)
                selected_cell = grid[r][c]

                if not is_start and selected_cell.path == True and selected_cell.end == False:
                    start_cell = selected_cell
                    selected_cell.start = True
                    is_start = True

            if pygame.mouse.get_pressed()[2]:  # right click to set end cell

                mouse_pos = pygame.mouse.get_pos()
                r, c = get_mouse_pos(mouse_pos, ROWS, WIDTH)
                selected_cell = grid[r][c]

                if not is_end and selected_cell.path == True and selected_cell.start == False:
                    end_cell = selected_cell
                    selected_cell.end = True
                    is_end = True

            if event.type == pygame.KEYDOWN:
                # press space to running path finding algorithm
                if event.key == pygame.K_SPACE and start_cell and end_cell:
                    for row in grid:
                        for cell in row:
                            cell.get_neighbors(grid)
                    path_found = astar(grid, start_cell, end_cell)  # run astar algorithm to find the shortest path
                    if not path_found:
                        pygame.display.set_caption("Path not found")
                    else:
                        pygame.display.set_caption("Shortest path found")

main()
