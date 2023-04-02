<template>
  <div class="grid-container">
    <Board v-if="state" :game="state.game" :tiles="state.tiles" :handler="handler"/>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import Board from './Board.vue'

const BACKEND = "http://localhost:8000"

export default {
  name: 'App',

  components: {
    Board
  },
  data() {
    return {
      state: {
        game: null,
        tiles: null
      },
      poller: 0    
    }
  },
  methods: {
    handler: function(index:number) {
      axios.post(BACKEND + `/game/flip/10/test1/${index}/`)
      .then(response => console.log(response))
      .then(_ => this.poll)
      .catch(error => {
        console.error(error);
      });
    },
    poll: function() {
      axios.get(BACKEND + `/game/10/`)
      .then(response => {
        this.state = response.data
      })
    }
  },
  mounted() {
    this.poller = setInterval(this.poll, 500)
  },
  unmounted() {
    clearInterval(this.poller)
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

