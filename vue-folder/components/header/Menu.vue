<template>
  <transition name="menu">
    <aside v-if="menu.showMenu">
      <menu-user-info/>
      <menu-list v-bind:menuItems="menuItems"/>
    </aside>
  </transition>
</template>

<script>
  import MenuList from './MenuList';
  import MenuUserInfo from './MenuUserInfo';

  export default {
    name: "Menu",
    components: {
      MenuList,
      MenuUserInfo
    },
    props: {
      menu: {
        type: Object,
        required: true
      },
      menuItems: {
        type: Array,
        required: true
      }
    }
  }
</script>

<style scoped>
  aside {
    margin-top: 40px;
    position: fixed;
    top: 0;
    left: 0;
    width: 250px;
    background: #087E8B;
    height: 100%;
    z-index: 2;
  }

  .menu-enter-active, .menu-leave-active {
    transition: all .8s cubic-bezier(.65, .05, .36, 1);
  }

  .menu-enter {
    left: -100%;
  }

  .menu-leave-to {
    left: -100%;
  }
</style>