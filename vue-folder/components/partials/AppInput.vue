<template>
  <div>
    <label v-bind:for="id">{{ label }}</label>
    <br/>
    <input v-bind:type="type" v-bind:id="id" v-bind:name="id"/>
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
  div {
    margin: 10px;

    input {
      border-radius: 10px;
      border: 2px solid #087e8b;
      outline: none;
      padding: 0 10px;
      height: 28px;
      font-size: 16px;
    }
  }
</style>
