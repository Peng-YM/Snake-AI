# coding: utf-8
from Tkinter import *
from random import randint
import numpy as np
import time

# some constants
COLORS = ['white', 'black', 'red', 'blue', 'grey', 'white']
EMPTY = 0
BODY = 1
FOOD = 2
HEAD = 3
WALL = 4
# board
BOARD = np.array([
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 2, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
])
HEIGHT = len(BOARD)
WIDTH = len(BOARD[0])
# Array that represents the snake. First element is the head of snake.
default_location = [(5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (6, 11),
                    (7, 11), (7, 10), (7, 9)]
# Initial position of the snake
food = (5, 1)
# GUI Parameters
CELL_WIDTH = 40
width = len(BOARD[0]) * CELL_WIDTH
height = len(BOARD) * CELL_WIDTH

# functions to get every direction of position x
LEFT = lambda x: (x[0], x[1] - 1)
RIGHT = lambda x: (x[0], x[1] + 1)
UP = lambda x: (x[0] - 1, x[1])
DOWN = lambda x: (x[0] + 1, x[1])


# snake class
class Snake:
    def __init__(self, board, locations=default_location, speed=0, virtual=False):
        self.locations = locations
        self.speed = speed
        self.board = board
        self.virtual = virtual
        self.score = 0

    def head(self):
        return self.locations[0]

    def tail(self):
        return self.locations[-1]

    # move one step forward the given direction
    def move(self, direction):
        head = [direction(self.head())]
        self.board[self.tail()] = EMPTY
        temp = self.tail()
        # move the snake
        self.locations = head + self.locations[:-1]
        if self.head() == food:
            # the snake grow one block
            self.locations = self.locations + [temp]
            # regenerate the food
            self.generate_food()
            self.score += 1
        if not self.virtual:
            time.sleep(self.speed)
        self.update_board()

    # update board
    def update_board(self):
        for block in self.locations:
            self.board[block] = BODY
        self.board[self.head()] = HEAD
        self.board[food] = FOOD
        if not self.virtual:
            self.draw()

    # place food randomly
    def generate_food(self):
        global food
        while True:
            loc = (randint(0, HEIGHT - 1), randint(0, WIDTH - 1))
            if self.board[loc] == EMPTY:
                food = loc
                break

    # validate a movement
    def validate_move(self, location, direction):
        if location[0] >= len(self.board) or location[1] >= len(self.board[0])\
                or location[0] < 0 or location[1] < 0:
            return False
        else:
            next_loc = self.board[direction(location)]
            return next_loc == EMPTY or next_loc == FOOD

    # get valid directions
    def get_valid_moves(self, location):
        movement = []
        for d in [LEFT, RIGHT, UP, DOWN]:
            if self.validate_move(location, d):
                movement.append(d)
        return movement

    # draw GUI
    def draw(self):
        canvas.delete('all')
        canvas.config(width=width, height=height)
        for i in range(len(self.board[0])):
            for j in range(len(self.board)):
                index = self.board[j][i]
                color = COLORS[index]
                cell_x = i * CELL_WIDTH
                cell_y = j * CELL_WIDTH
                canvas.create_rectangle(cell_x, cell_y, cell_x + CELL_WIDTH, cell_y + CELL_WIDTH,
                                        fill=color, outline='white')
        canvas.update()

    def alive(self):
        return len(self.get_valid_moves(self.head())) > 0

    def A_star(self, source):
        global food
        result = self.board.copy()
        result[result != EMPTY] = -1
        distance = 0
        queue = list()
        queue.append(source)
        visited = set()
        while len(queue) > 0:
            p = queue.pop(0)
            visited.add(p)
            distance += 1
            for d in self.get_valid_moves(p):
                if d(p) not in visited:
                    queue.append(d(p))
                    visited.add(d(p))
                    result[d(p)] = distance
        return result

    def chase_food(self):
        distances = self.A_star(food)
        head = self.head()
        shortest_move = None
        min_distance = float('inf')
        for d in self.get_valid_moves(head):
            dis = distances[d(head)]
            if dis < min_distance:
                min_distance = dis
                shortest_move = d
        return shortest_move

    def chase_tail(self):
        distances = self.A_star(self.tail())
        head = self.head()
        longest_move = None
        max_distance = -float('inf')
        for d in self.get_valid_moves(head):
            dis = distances[d(head)]
            if dis > max_distance:
                max_distance = dis
                longest_move = d
        return longest_move

    # is it safe to eat the food?
    def safe_to_eat(self):
        global food
        new_environment = self.board.copy()
        new_locations = [l for l in self.locations]
        original_food = food
        virtual_snake = Snake(new_environment, new_locations, virtual=True)
        while virtual_snake.alive() and original_food == food:
            m = virtual_snake.chase_food()
            virtual_snake.move(m)
        food = original_food
        if virtual_snake.has_path_to(virtual_snake.head(), virtual_snake.tail()):
            return True
        else:
            return False
    
    def has_path_to(self, source, goal):
        has_path = False
        result = self.A_star(goal)
        for d in self.get_valid_moves(source):
            if result[d(source)] > 0:
                has_path = True
        return has_path

    def distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) - 1

    def run(self):
        while self.alive():
            if self.has_path_to(self.head(), food):
                if self.safe_to_eat():
                    m = self.chase_food()
                else:
                    m = self.chase_tail()
            else:
                m = self.chase_tail()
            self.move(m)
        print 'Score: ', self.score

if __name__ == '__main__':
    root = Tk()
    root.title('Snake AI')
    canvas = Canvas(root, bg="white")
    canvas.pack()
    s = Snake(BOARD)
    s.run()
    # close the main window
    root.mainloop()
