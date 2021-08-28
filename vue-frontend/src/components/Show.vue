<template>
  <!-- PART 4: Add your code here -->
  <div>
    <h3>{{name}}</h3>
    <Counter
      counter_name="Episodes watched"
      v-bind:count="episodes_seen"
    />
  <br />
  </div>
</template>

<script>
// PART 4: Add your code here
import Counter from "./Counter.vue"
export default {
  components: {
    Counter
  },
  props: {
    id: Number,
    name: String,
    episodes_seen: Number
  }
};
</script>

<style>
</style>
~               
