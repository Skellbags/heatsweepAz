<template>
  <button class="square" :class="statusClass" @click="handleClick">
    {{ cellColor }}
  </button>
</template>

<script>
export default {
  props: ['cell', 'onClick'],
  computed: {
    statusClass() {
      return 'status-' + this.cell.status;
    },
    cellColor() {
      switch (this.cell.heatValue) {
        case 0:
          return '';
        case 1:
          return '🔥';
        case 2:
          return '🔥🔥';
        case 3:
          return '🔥🔥🔥';
        default:
          return '';
      }
    },
  },
  methods: {
    handleClick() {
      this.onClick(this.cell);
    },
  },
};
</script>

<style scoped>
.square {
  background: #fff;
  border: 1px solid #999;
  float: left;
  font-size: 24px;
  font-weight: bold;
  line-height: 34px;
  height: 34px;
  margin-right: -1px;
  margin-top: -1px;
  padding: 0;
  text-align: center;
  width: 34px;
}

.square.status-none {
  background: #fff;
}

.square.status-player_a {
  background: #aaf;
}

.square.status-player_b {
  background: #faa;
}
</style>
