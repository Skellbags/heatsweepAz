<template>
  <div class="board">
    <div class="grid">
      <button
        v-for="(tile, index) in tiles"
        :key="index"
        @click="handler.click(index)"
        :disabled="tile.status == "
      >
        {{ tile.status }}
      </button>
    </div>
    <p v-if="winner">{{ winner }}</p>
  </div>
</template>
<script lang="ts">
import axios from 'axios';
import { defineComponent, reactive } from 'vue';

interface GridCell {
  status: string,
  index: number,
  heat_value: number
}

export default defineComponent({
  name: 'SquareGrid',
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
  },
  setup() {
    const BACKEND = "http://localhost:8000"
    const FLIP_EP = BACKEND + "/game/flip/10/test1/"
    this.handler = (index) => {
      axios.post(FLIP_EP + `${index}/`)
      .catch(error => {
        console.error(error);
      });
    }

    const state = reactive<GridData>({
      grid: [],
    });

    axios.get('/api/data/')
      .then(response => {
        state.grid = response.data.grid;
      })
      .catch(error => {
        console.error(error);
      });

    const getSquareStyle = (value: number) => {
      let color = 'white';
      if (value === 0) {
        color = 'white';
      } else if (value === 1) {
        color = 'blue';
      } else if (value === 2) {
        color = 'red';
      } else if (value === 3) {
        color = 'yellow';
      }
      return {
        backgroundColor: color,
      };
    };

    return {
      grid: state.grid,
      getSquareStyle,
    };
  },
});
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(10, 3rem);
  grid-template-rows: repeat(10, 3rem);
  grid-gap: 0.3rem;
}
button {
  font-size: 1rem;
  font-family: monospace;
}
</style>
