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
            url: "/apothecary/goods",
            text: "Товары"
          },
          {
            url: "/apothecary/recipes",
            text: "Рецепты"
          }
        ]
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
