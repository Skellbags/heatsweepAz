from rest_framework import serializers

from .models import Player, Game, Tile

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'player_a', 'player_b', 'current_turn', 'winner')
        depth = 1

class TileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tile
        fields = ('status', 'x', 'y', 'heat_value')