<template>
  <div class="board">
    <div v-if="game && game.player_a" class="player-info-container">
      <h2>Player A <span style="color: #008f39">◼</span></h2>
      <h3>Username: {{ game.player_a.username }}</h3>
    </div>
    <div class="grid">
      <button :class="['board-tile', tile.status == 'a' ? 'a-tile' : (tile.status == 'b' ? 'b-tile' : '')]"
          :style="{'background-color': tile.heat_value}"
          v-for="(tile, index) in tiles"
          :key="index"
          @click="handler(index)"
      >
      </button>
    </div>
    <div v-if="game && game.player_b" class="player-info-container">
      <h2>Player B<span style="color: #944dff">◼</span></h2>
      <h3>Username: {{ game.player_b.username }}</h3>
    </div>
    <h1 v-if="winner">{{ winner }}</h1>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Board',
  props: {
    game: null,
    tiles: null,
    handler: null
  },
  data() {

  },
  computed: {
    winner() {
      if (!this.game || !this.game.winner) return;
      return `Player ${this.game.winner.username} wins!`;
    },
  },
  methods: {
    computeColor(val: number) {
      var r = 255
      var g = 255 * val
      var b = g
      return `#${r.toString(16)}${g.toString(16)}${b.toString(16)}`
    }
  }
});
</script>

<style scoped>
h1 {
    font-size: 30px;
    text-align: center;
}
.grid {
  display: grid;
  grid-template-columns: repeat(7, 3rem);
  grid-template-rows: repeat(7, 3rem);
  grid-gap: 0.3rem;
}
button {
  font-size: 1rem;
  font-family: monospace;
}
.a-tile {
  border-color: #008f39
}
.b-tile {
  border-color: #944dff
}
.board-tile {
  border-radius: 4px;
  border-style: solid;
  border-width: 4px;
  cursor: pointer;
}
</style>
