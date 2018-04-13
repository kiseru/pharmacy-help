<template>
  <button type="submit">{{ name }}</button>
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
    background-color: #087e8b;
    border: 2px solid #087e8b;
    border-radius: 5px;
    color: #ffffff;
    margin: 15px auto;
    font-size: 18px;
    width: 100px;
    height: 36px;
    outline: none;
    transition: ease .8s;

    &:hover {
      background-color: #ffffff;
      color: #087e8b;
    }
  }
</style>
