<template>
  <button id="menu-button" v-on:click="menu.showMenu = !menu.showMenu">
    <span class="ion-navicon"></span>
  </button>
</template>

<script>
  export default {
    name: "BurgerButton",
    props: {
      menu: {
        type: Object,
        required: true
      }
    }
  }
</script>

<style lang="less" scoped>
  #menu-button {
    position: relative;
    height: 56px;
    width: 56px;
    padding: 3px;
    transition: ease 0.3s;
    z-index: 2;
    background-color: #343a40;
    border: 0;
    outline: none;

    span {
      color: #F5f5f5;
      font-size: 26px;
    }

    &:hover {
      background-color: #f5f5f5;

      span {
        color: #343a40;
      }
    }
  }
</style>
