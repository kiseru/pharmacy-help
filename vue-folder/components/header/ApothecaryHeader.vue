<template>
  <app-header v-bind:menu-items="menuItems"/>
</template>

<script>
  import AppHeader from "./Header";

  export default {
    name: "ApothecaryHeader",
    components: {
      AppHeader
    },
    data() {
      return {
        menuItems: [
          {
            url: "/goods",
            text: "Товары"
          },
          {
            url: "/recipes",
            text: "Рецепты"
          },
          {
            url: "/logout",
            text: "Выйти"
          }
        ]
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
