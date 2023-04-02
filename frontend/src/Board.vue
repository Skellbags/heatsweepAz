<template>
  <div class="board">
    <!-- <h1>Game Board (#{{ game.id }})</h1> -->
    <div class="grid">
      <button
        v-for="(tile, index) in tiles"
        :key="index"
        @click="handler(index)"
      >
        {{ tile.status == "none" ? "" : tile.status }}
      </button>
    </div>
    <p v-if="winner">{{ winner }}</p>
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
  computed: {
    winner() {
      if (!this.game || !this.game.winner) return;
      return `Player ${this.game.winner.username} wins!`;
    },
  }
});
</script>

<style scoped>
h1 {
    font-size: 50px;
    text-align: center;
}
.grid {
  display: grid;
  grid-template-columns: repeat(5, 3rem);
  grid-template-rows: repeat(5, 3rem);
  grid-gap: 0.3rem;
}
button {
  font-size: 1rem;
  font-family: monospace;
}
</style>
