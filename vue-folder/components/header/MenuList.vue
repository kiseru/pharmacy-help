<template>
  <div id="menu-list">
    <menu-list-item v-for="item in menuItems" v-bind:item="item"/>
  </div>
</template>

<script>
  import MenuListItem from './MenuListItem';

  export default {
    name: "MenuList",
    components: {
      MenuListItem
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
  #menu-list {
    width: inherit;
    height: auto;
    margin-top: 20px;
  }
</style>