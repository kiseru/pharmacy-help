<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark pb-0">
    <burger-button v-bind:menu="menu" class="navbar-text navbar-brand"/>
    <a href="/" class="navbar-brand">Pharmacy Help</a>
    <div class="navbar-collapse offcanvas-collapse">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item active text-light">{{ user.first_name }} {{ user.last_name }}</li>
      </ul>
    </div>
    <app-menu v-bind:menu="menu" v-bind:menuItems="menuItems"/>
  </nav>
</template>

<script>
  import axios from 'axios';

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
        },
        user: {
          firstName: "NotFound",
          lastName: ""
        }
      }
    },
    props: {
      menuItems: {
        type: Array,
        required: true
      }
    },
    beforeMount() {
      axios.get("/api/user")
        .then(response => this.user = response.data)
        .catch(error => this.user = {
          first_name: "",
          last_name: "Not Found"
        });
    }
  }
</script>

<style lang="less" scoped>
  nav {
    height: 56px;
    padding: 0 16px 8px 0;
    position: fixed;
    z-index: 1;
    top: 0;
    left: 0;
    right: 0;
  }
</style>
