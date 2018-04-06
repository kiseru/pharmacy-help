<template>
  <div id="header">
    <burger-button v-bind:menu="menu"/>
    <logo/>
    <app-menu v-bind:menu="menu" v-bind:menuItems="menuItems"/>
  </div>
</template>

<script>
  import BurgerButton from './MenuButton';
  import Logo from './Logo';
  import AppMenu from './Menu';

  export default {
    name: "Header",
    components: {
      BurgerButton,
      Logo,
      AppMenu
    },
    data() {
      return {
        menu: {
          showMenu: false
        }
      }
    },
    props: {
      menuItems: {
        type: Array,
        required: true
      }
    }
  }
</script>

<style scoped>
  #header {
    display: inline-flex;
    position: relative;
    top: 0;
    width: 100%;
    height: 40px;
    background-color: #087E8B;
    text-align: center;
    z-index: 1;
  }
</style>