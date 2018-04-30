<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <burger-button v-bind:menu="menu" class="navbar-text navbar-brand"/>
    <a href="/" class="navbar-brand">Pharmacy Help</a>
    <app-menu v-bind:menu="menu" v-bind:menuItems="menuItems"/>
  </nav>
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

<style lang="less" scoped>
  nav {
    height: 56px;
    padding: 8px 16px 8px 0;
  }
</style>
