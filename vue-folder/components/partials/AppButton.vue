<template>
  <button type="submit" class="btn btn-primary">{{ name }}</button>
</template>

<script>
  export default {
    name: "AppButton",
    props: {
      name: {
        required: true
      }
    }
  }
</script>

<style lang="less" scoped>
  button {
    margin: 15px auto;
  }
</style>
