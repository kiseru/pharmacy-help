<template>
  <div class="form-group">
    <label v-bind:for="id">{{ label }}</label>
    <input v-bind:type="type" class="form-control" v-bind:id="id" v-bind:name="id"/>
  </div>
</template>

<script>
  export default {
    name: "AppInput",
    props: {
      id: {
        required: true
      },
      label: {
        required: true
      },
      type: {
        required: false,
        default: "text"
      }
    }
  }
</script>

<style lang="less" scoped>
</style>
