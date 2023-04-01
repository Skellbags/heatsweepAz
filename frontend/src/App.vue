<template>
  <div class="grid-container">
    <SquareC v-for="(cell, index) in formattedGrid" :key="index" :color="cell"/>
  </div>
</template>

<script>
import { computed } from 'vue'
import Board from './Board'
import SquareC from './SquareC.vue'

export default {
  name: 'App',

  components: {
    SquareC
  },

  setup() {
    const { grid } = Board()

    const formattedGrid = computed(() => {
      return grid.map(row => {
        return row.map(cell => {
          switch (cell) {
            case 0:
              return 'white'
            case 1:
              return 'red'
            case 2:
              return 'green'
            case 3:
              return 'blue'
          }
        })
      })
    })

    return {
      formattedGrid
    }
  }
}
</script>

<style>
.grid-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.row {
  display: flex;
}

.cell {
  width: 50px;
  height: 50px;
  margin: 2px;
}
</style>

