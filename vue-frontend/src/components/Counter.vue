<template>
  <div id="count-buttons">
    <p>{{counter_name}}: {{ count }}.</p>
    <button v-on:click="count += 1">Increment</button>
    <button v-on:click="count -= 1">Decrement</button>
  </div>
</template>

<script>
export default {
  name: 'count-buttons',
  props: {
    count: {
      type: Number,
      default: 0
    },
    counter_name: {
      type: String,
      default: "Current count"
    }
  }
};
</script>

<style>
</style>

