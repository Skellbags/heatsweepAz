from random import randrange
from enum import Enum
from django.db import models

# class syntax
class Color(Enum):
    P1 = 1
    P2 = 2
    HOTSPOT = 3

class Board(models.Model):

    gridSize = models.IntegerField()
    p1_start_x = models.IntegerField()
    p1_start_y = models.IntegerField()
    p2_start_x = models.IntegerField()
    p2_start_y = models.IntegerField()
    hot_spot_x = models.IntegerField()
    hot_spot_y = models.IntegerField()

    def __init__(self, gridSize, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.gridSize = gridSize
        self.grid = []
        row = []
        for _ in range(0, gridSize):
            for _ in range(0, gridSize):
                row.append(Point())
            self.grid.append(row)
            row = []

        bounds = [0, gridSize-1]

        self.p1_start_x = bounds[randrange(0,2)]
        self.p1_start_y = bounds[randrange(0,2)]
        self.p2_start_x = bounds[randrange(0,2)]
        self.p2_start_y = bounds[randrange(0,2)]

        while self.p1_start_x == self.p2_start_x and self.p1_start_y == self.p2_start_y:
            self.p2_start_x = bounds[randrange(2)]
            self.p2_start_y = bounds[randrange(2)]

        self.hot_spot_x = randrange(0,9)
        self.hot_spot_y = randrange(0,9)
        while self.hot_spot_x == self.p1_start_x and self.hot_spot_y == self.p1_start_y or \
            self.hot_spot_x == self.p2_start_x and self.hot_spot_y == self.p2_start_y:
            self.hot_spot_x = randrange(0,9)
            self.hot_spot_y = randrange(0,9)

    def initialize_board(self):
        self.flip(self.p1_start_x, self.p1_start_y, Color.P1)
        self.flip(self.p2_start_x, self.p2_start_y, Color.P2)

    def flip(self, x, y, p):
        spot = (x,y)
        if spot == (self.hot_spot_x, self.hot_spot_y):
            self.grid[y][x].value = Color.HOTSPOT.value
        else:
            self.grid[y][x].value = p.value
        
class Point(models.Model):
    value = models.IntegerField(default=0)
