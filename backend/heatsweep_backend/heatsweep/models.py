from django.db import models
from random import randrange

class Player(models.Model):
    username = models.TextField(unique=True, max_length=20)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    elo = models.IntegerField(default=1000)

class Tile(models.Model):
    NONE = 'none'
    A = 'a'
    B = 'b'
    H = 'hotspot'
    TILE_CHOICES = (
        (NONE, 'None'),
        (A, 'A'),
        (B, 'B'),
        (H, 'Hotspot'),
    )
    status = models.CharField(max_length=6, choices=TILE_CHOICES, default=NONE)
    x = models.IntegerField()
    y = models.IntegerField()
    heat_value = models.FloatField(default=0.0)
    game = models.ForeignKey('heatsweep.Game', related_name="tile_game")

    def flip(self, status):
        if (self.status != Tile.NONE):
            return False
        else:
            self.status = status
            self.save(update_fields=['status'])
            return True

class Game(models.Model):
    GRID_SIZE = 10
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

    def get_all_tiles(self):
        return Tile.objects.filter(game=self)

    def get_tile_at(self, x, y):
        try:
            return Tile.objects.get(game=self, x=x, y=y)
        except Tile.DoesNotExist:
            return None

    def flip(self, x, y, player):
        if (self.current_turn != player):
            return False

        tile = self.get_tile_at(x, y)

        status = Tile.A
        if (x == self.hotspot.x and y == self.hotspot.y):
            status = Tile.H
        elif(player == self.player_b):
            status = Tile.B

        if not tile.flip(status):
            return False

        self.next_turn()
        self.save()
        return True

    def init_start_points(self):
        bounds = [0, Game.GRID_SIZE-1]

        a_x = bounds[randrange(0,2)]
        a_y = bounds[randrange(0,2)]
        b_x = bounds[randrange(0,2)]
        b_y = bounds[randrange(0,2)]

        while a_x == b_x and a_y == b_y:
            b_x = bounds[randrange(2)]
            b_y = bounds[randrange(2)]

        self.a_start = self.get_tile_at(a_x, a_y)
        self.a_start.flip(Tile.A)

        self.b_start = self.get_tile_at(b_x, b_y)
        self.b_start.flip(Tile.B)

        h_x = randrange(0, Game.GRID_SIZE-(Game.MARGIN*2)-1) + Game.MARGIN
        h_y = randrange(0, Game.GRID_SIZE-(Game.MARGIN*2)-1) + Game.MARGIN

        self.hotspot = self.get_tile_at(h_x, h_y)

    def next_turn(self):
        current_turn = self.player_a if current_turn == self.player_b else self.player_b
