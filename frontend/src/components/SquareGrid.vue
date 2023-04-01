thods: {
    getSquareStyle(value) {
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
<template>
  <div class="square-grid">
    <div v-for="(row, rowIndex) in grid" :key="rowIndex" class="square-row">
      <div v-for="(value, columnIndex) in row" :key="columnIndex" :style="getSquareStyle(value)" class="square">{{ value }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import { defineComponent, reactive } from 'vue';

interface GridData {
  grid: number[][];
}

export default defineComponent({
  name: 'SquareGrid',
  setup() {
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

<style>
.square-grid {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.square-row {
  display: flex;
}

.square {
  width: 30px;
  height: 30px;
  margin: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}
</style>

