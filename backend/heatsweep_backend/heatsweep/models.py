from django.db import models
from random import randrange

class Player(models.Model):
    username = models.TextField(unique=True, max_length=20)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    elo = models.IntegerField(default=1000)

class Tile(models.Model):
    EMPTY = 'none'
    A = 'a'
    B = 'b'
    H = 'hotspot'
    TILE_CHOICES = (
        (EMPTY, 'None'),
        (A, 'A'),
        (B, 'B'),
        (H, 'Hotspot'),
    )
    status = models.CharField(max_length=6, choices=TILE_CHOICES, default=EMPTY)
    x = models.IntegerField()
    y = models.IntegerField()
    heat_value = models.FloatField(default=0.0)
    a_revealed = models.BooleanField(default=False)
    b_revealed = models.BooleanField(default=False)
    game = models.ForeignKey('heatsweep.Game', related_name="tile_game")

    '''
    Setter method to update the status of a Tile
    Automatically reveals the tile to player 1/player 2 if they are set as the new owner
    '''
    def set_status(self, status):
        # check if anything needs to be updated first
        if status != self.status:
            self.status = status
            self.save(update_fields=['status'])

            # reveal the tile if applicable
            if status == Tile.A:
                self.reveal_a()
            elif status == Tile.B:
                self.reveal_b()
        return True
    
    '''
    Reveals the tile to player a.
    '''
    def reveal_a(self):
        if not self.a_revealed:
            self.a_revealed = True
            self.save(update_fields=['p1shown'])
        return True
    
    '''
    Reveals the tile to player b.
    '''
    def reveal_b(self):
        if not self.b_revealed:
            self.b_revealed = True
            self.save(update_fields=['p2shown'])
        return True
    
    '''
    Reveals the tile to the given player.
    '''
    def reveal(self, player):
        if player == self.A:
            self.reveal_a()
        elif player == self.B:
            self.reveal_b()
        else:
            raise ValueError("invalid player value passed to Tile.reveal()")
        
    '''
    Getter method for the revealed state of the tile.
    '''
    def revealed(self, player):
        if player == self.A:
            return self.a_revealed
        elif player == self.B:
            return self.b_revealed
        else:
            raise ValueError("invalid player value passed to Tile.reveal()")

class Game(models.Model):
    GRID_SIZE = 10
    GRID_X = 10
    GRID_Y = 10
    MARGIN = 3
    player_a = models.ForeignKey(Player, related_name="game_player_a", null=True, blank=True)
    player_b = models.ForeignKey(Player, related_name="game_player_b", null=True, blank=True)
    current_turn = models.ForeignKey(Player, related_name="game_turn", null=True, blank=True)
    winner = models.ForeignKey(Player, related_name='game_winner', null=True, blank=True)
    
    hotspot = models.ForeignKey(Tile, related_name='game_hotspot', null=True, blank=True)
    a_start = models.ForeignKey(Tile, related_name='game_a_start', null=True, blank=True)
    b_start = models.ForeignKey(Tile, related_name='game_b_start', null=True, blank=True)

    @staticmethod
    def create(player):
        game = Game(player_a=player, current_turn=player)
        game.save()
        for x in range(Game.GRID_SIZE):
            for y in range(Game.GRID_SIZE):
                tile = Tile(x=x, y=y, game=game)
                tile.save()
        game.init_start_points()

        return game     

    '''
    Converts a player string, such as 'a', or 'b', to its corresponding Tile status value. 
    '''
    @staticmethod
    def toStatus(player: str):
        if player == 'a':
            return Tile.A
        elif player == 'b':
            return Tile.B
        else:
            raise ValueError("passing invalid player to toStatus")

    def get_all_tiles(self):
        return Tile.objects.filter(game=self)

    def get_tile_at(self, x, y):
        try:
            return Tile.objects.get(game=self, x=x, y=y)
        except Tile.DoesNotExist:
            return None

    '''
    Sets ownership (status) of the specified tile to the specified player. If the specified tile is the hotspot, set its 
    status to the hotspot. This happens because at the beginning of the game, the hotspot doesn't appear on the board;
    only its coordinates are saved.

    This is the basic, non-fog-of-war approach.
    '''
    def flip(self, x, y, player):
        if (self.current_turn != player):
            return False

        tile = self.get_tile_at(x, y)

        if (x == self.hotspot.x and y == self.hotspot.y):
            status = Tile.H
        elif (player == self.player_a):
            status = Tile.A
        elif (player == self.player_b):
            status = Tile.B

        if not tile.set_status(status):
            return False

        self.next_turn()
        self.save()
        return True

    def init_start_points(self):
        # initialize grid
        for _ in range(0, self.GRID_Y):
            row = []
            for _ in range(0, self.GRID_X):
                row.append(Tile())
            self.grid.append(row)

        # randomly pick player starting points and set the status of their tiles
        # both points in middle half, a is on top 4th, b bottom 4th
        self.a_x = randrange(self.GRID_X/4,3*self.GRID_X/4-1)
        self.a_y = randrange(0,self.GRID_Y/4)
        self.b_x = randrange(self.GRID_X/4,3*self.GRID_X/4-1)
        self.b_y = randrange(0,self.GRID_Y/4)
        self.get_tile_at(self.a_x, self.a_y).set_status(Tile.A)
        self.get_tile_at(self.a_x, self.a_y).set_status(Tile.B)

        # TODO TODO TODO: get rid of these? a_start, b_start, and hotspot all seem unnecessary
        self.a_start = self.get_tile_at(self.a_x, self.a_y)
        self.a_start.set_status(Tile.A)

        self.b_start = self.get_tile_at(self.b_x, self.b_y)
        self.b_start.set_status(Tile.B)

        # TODO TODO TODO: updpate to better hotspot algorithm below
        self.h_x = randrange(0, Game.GRID_SIZE-(Game.MARGIN*2)-1) + Game.MARGIN
        self.h_y = randrange(0, Game.GRID_SIZE-(Game.MARGIN*2)-1) + Game.MARGIN

        '''
        # hotspot should be equidistant from both players
        # all points on the line perpendicular to (a_x, a_y) -- (b_x, b_y) satisfy this constraint
        # pick an offset from the midpoint of that line at random and do the math
        # TODO: this technically needs integer solutions to be perfectly fair always. Otherwise off by 1
        # first pick the x-coord of the hotspot, then find the y-coord using point-slope form
        midpoint = ((self.b_x - self.a_x)/2, (self.b_y - self.a_y)/2)
        self.h_x = randrange(-self.GRID_X/4, self.GRID_X/4)
        slope = -self.a_x/self.a_y
        self.h_y = slope(self.h_x - midpoint.first) + midpoint.second 
        '''

        self.hotspot = self.get_tile_at(self.h_x, self.h_y) # TODO TODO TODO: get rid of this?
        # self.hotspot.set_status(Tile.H) TODO: readd this once fog of war comes back

    '''
    Returns a list of the coordinates adjacent to (x, y) that are within the grid.
    '''
    def valid_adjacent_coords(self, x, y):
        coords = []
        for (xi, yi) in [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]:
            if 0 <= xi < self.GRID_X and 0 <= yi < self.GRID_Y: 
                coords.append(xi, yi)
        
    '''
    Reveals tiles adjacent to (x, y) to the given player.
    '''
    def reveal_adjacent(self, x, y, player):
        for (xi, yi) in self.valid_adjacent_coords(x, y):
            self.get_tile_at(xi, yi).reveal(player)

    '''
    Gives input player ownership of any unowned tiles adjacent to the tile at (x, y).
    '''
    def flip_adjacent(self, x, y, player):
        for (xi, yi) in self.valid_adjacent_coords(x, y):
            tile = self.get_tile_at(xi, yi)
            if tile.status == Tile.EMPTY:
                tile.set_status(self.toStatus(player))
            self.reveal_adjacent(xi, yi, player)

    '''
    Gives player ownership of tile at (x, y). If that tile is unowned (and not the hotspot), 
    flip any unowned adjacent tiles as well.

    All tiles adjacent to those just flipped will be revealed to the player as well.

    Note: "adjacent" does not include diagonals here.
    '''
    def flipFogOfWar(self, x, y, player):
        tile = self.get_tile_at(x, y) # get the tile

        # if this grid space is empty, flip adjacent tiles as well (not diagonal)
        if tile.status == Tile.EMPTY:
            self.flip_adjacent(x, y, player)
        
        tile.set_status(self.toStatus(player)) # flip the tile

    # =+++++++++++++++++=
    # WIN CONDITION LOGIC
    # =+++++++++++++++++=

    # grid of 0s
    def empty_grid(self):
        return [[0]*self.GRID_X for _ in range(self.GRID_Y)]

    # return a list of all the coords within a 3x3 square around (x,y) if in the grid
    # I'm sure there's a cleaner way to do this but honestly this is the most readable I can do
    def get_adjacent(self, x, y):
        coords = []
        for xi in [x-1, x, x+1]:
            for yi in [y-1, y, y+1]:
                if 0 <= xi < self.GRID_X and 0 <= yi < self.GRID_Y: # make sure coords within grid
                    coords.append((xi, yi))
        return coords

    def process_adjacent(self, x, y, player, checked):
        checked[y][x] = 1 # mark current coord as checked
        for (xi, yi) in self.get_adjacent(x, y):
            # base case: hotspot is adjacent to us
            if (xi, yi) == (self.h_x, self.h_y):
                return True
            
            if checked[yi][xi] == 0 and self.get_tile_at(xi, yi).status == player:
                # recurse on adjacent un-checked squares owned by player
                if self.process_adjacent(xi, yi, player, checked):
                    return True
        
        # base case: no path to hotspot
        return False

    def check_win(self, player: str):
        # step 0: check if the player can see the hotspot
        if not self.get_tile_at(self.h_x, self.h_y).revealed(player):
            return False
        
        # recursively build out pathway from hotspot
        checkedGrid = self.empty_grid() # initialize matrix of 0s
        if player == self.player_a:
            return self.process_adjacent(self.a_x, self.a_y, self.player_a, checkedGrid)
        elif player == self.player_b:
            return self.process_adjacent(self.b_x, self.b_y, self.player_b, checkedGrid)
        
    def next_turn(self):
        if self.check_win(self.current_turn):
            self.winner = self.current_turn

        current_turn = self.player_a if current_turn == self.player_b else self.player_b

    
