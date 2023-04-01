from random import randrange
from enum import Enum
from django.db import models
import numpy as np

# class syntax
class Ownership(Enum):
    EMPTY = 0
    P1 = 1
    P2 = 2
    HOTSPOT = 3


class Board(models.Model):

    gridSize = models.IntegerField()
    (p1x, p1y) = (models.IntegerField(), models.IntegerField())
    (p2x, p2y) = (models.IntegerField(), models.IntegerField())
    (hx, hy) = (models.IntegerField(), models.IntegerField())

    def __init__(self, gridX, gridY, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.gridX = gridX
        self.gridY = gridY

        # initialize grid
        # VERY IMPORTANT TODO TODO TODO:
        # TODO TODO:
        # TODO:
        # change this from Point() to Tile() in later versions
        for _ in range(0, gridY):
            row = []
            for _ in range(0, gridX):
                row.append(Point())
            self.grid.append(row)

        # randomly pick player starting points
        # p1 is anywhere on top 4th of board, p2 bottom 4th
        self.p1x = randrange(gridX/4,3*gridX/4-1)
        self.p1y = randrange(0,gridY/4)
        self.p2x = randrange(gridX/4,3*gridX/4-1)
        self.p2y = randrange(0,gridY/4)

        # hotspot should be equidistant from both players
        # all points on the line perpendicular to (p1x, p1y) -- (p2x, p2y) satisfy this constraint
        # pick an offset from the midpoint of that line at random and do the math
        # TODO: this technically needs integer solutions to be perfectly fair always. Otherwise off by 1
        # first pick the x-coord of the hotspot, then find the y-coord using point-slope form
        midpoint = ((self.p2x - self.p1x)/2, (self.p2y - self.p1y)/2)
        self.hx = randrange(-gridX/4, gridX/4)
        slope = -self.p1x/self.p1y
        self.hy = slope(self.hx - midpoint.first) + midpoint.second 

    def initialize_board(self):
        self.flip(self.p1x, self.p1y, Ownership.P1)
        self.flip(self.p2x, self.p2y, Ownership.P2)

    def flip(self, x, y, p):
        spot = (x,y)
        if spot == (self.hx, self.hy):
            self.grid[y][x].value = Ownership.HOTSPOT.value
        else:
            self.grid[y][x].value = p.value
    
    def validAdjacentCoords(self, x, y):
        for (xi, yi) in [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]:
            yield (xi, yi) if 0 <= xi < self.gridX and 0 <= yi < self.gridY

    '''
    Reveals tiles adjacent to (x, y) to player.
    '''
    def revealAdjacent(self, x, y, player):
        for (xi, yi) in self.validAdjacentCoords(x, y):
            if player == 1:
                self.grid[yi][xi].p1shown = True
            else:
                self.grid[yi][xi].p2shown = True

    '''
    Gives input player ownership of any tiles adjacent to the tile at (x, y).
    '''
    def flipAdjacent(self, x, y, player):
        for (xi, yi) in self.validAdjacentCoords(x, y):
            if self.grid[yi][xi].ownership == Ownership.EMPTY.value:
                self.grid[yi][xi].ownership = player
                self.revealAdjacent(x, y, player)

    '''
    Gives player ownership of tile at (x, y). If that tile is unowned (and not the hotspot), 
    flip any unowned adjacent tiles as well.

    All tiles adjacent to those just flipped will be revealed to the player as well.

    Note: "adjacent" does not include diagonals here.
    '''
    def flipWithHiddenBoard(self, x, y, player):
        if player == 1:
            self.grid[y][x].p1shown = True
        if player == 2:
            self.grid[y][x].p2shown = True
        
        # if this grid space is empty, flip adjacent tiles as well (not diagonal)
        if self.grid[y][x].ownership == Ownership.EMPTY:
            self.flipAdjacent(x, y, player)

        self.grid[y][x].ownership = player

    
    # =++++++++++++++++=
    # LOGIC TO CHECK WIN 
    # =++++++++++++++++=

    # grid of 0s
    def emptyGrid(self):
        return [[0]*self.gridX for _ in range(self.gridY)]

    # return a list of all the coords within a 3x3 square around (x,y) if in the grid
    # I'm sure there's a cleaner way to do this but honestly this is the most readable I can do
    def getAdjacent(self, x, y):
        coords = []
        for xi in [x-1, x, x+1]:
            for yi in [y-1, y, y+1]:
                if 0 <= xi < self.gridX and 0 <= yi < self.gridY: # make sure coords within grid
                    coords.append((xi, yi))
        return coords

    def processAdjacent(self, x, y, player, checked):
        checked[y][x] = 1 # mark current coord as checked
        for (xi, yi) in self.getAdjacent(x, y):
            # base case: hotspot is adjacent to us
            if self.grid[yi][xi] == (self.hx, self.hy):
                return True
            
            if checked[yi][xi] == 0 and self.grid[yi][xi] == player:
                # recurse on adjacent un-checked squares owned by player
                if self.processAdjacent(xi, yi, player, checked):
                    return True
        
        # base case: no path to hotspot
        return False

    def checkWin(self, player: int):
        # step 0: check if the player can see the hotspot
        if player == 1:
            if not self.grid[self.hy][self.hx].p1shown:
                return False
        else:
            if not self.grid[self.hy][self.hx].p2shown:
                return False
        
        # recursively build out pathway from hotspot
        checkedGrid = self.emptyGrid() # initialize matrix of 0s
        if player == 1:
            return self.processAdjacent(self.p1x, self.p1y, 1, checkedGrid)
        else:
            return self.processAdjacent(self.p2x, self.p2y, 2, checkedGrid)
            
class Point(models.Model):
    value = models.IntegerField(default=0)

class Tile(models.Model):
    ownership = models.IntegerField(default=0)
    heat = models.IntegerField(default=0)
    p1shown = models.BooleanField(default=False)
    p2shown = models.BooleanField(default=False)