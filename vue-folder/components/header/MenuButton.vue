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

<style scoped>
  #menu-button {
    position: relative;
    height: 40px;
    width: 40px;
    padding: 3px;
    transition: ease 0.3s;
    z-index: 2;
    background-color: #087E8B;
    border: 0;
    outline: none;
  }

  span {
    color: #F5f5f5;
    font-size: 26px;
  }

  #menu-button:hover {
    background-color: #f5f5f5;
  }

  #menu-button:hover span {
    color: #087e8b;
  }

</style>