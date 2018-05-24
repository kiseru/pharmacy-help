<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <a href="/" class="navbar-brand">Pharmacy Help</a>
    <div class="navbar-collapse offcanvas-collapse">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item" v-if="user.is_admin">
          <a href="/workers" class="nav-link">Сотрудники</a>
        </li>
        <li class="nav-item" v-for="item in menuItems">
          <a v-bind:href="item.url" class="nav-link">{{item.text}}</a>
        </li>
        <li class="nav-item active text-light dropdown">
          <a href="#" class="nav-link dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{ user.first_name }} {{ user.last_name }}</a>
          <div class="dropdown-menu mt-1">
            <a href="/logout" class="dropdown-item">Выйти</a>
          </div>
        </li>
      </ul>
    </div>
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
</style>
