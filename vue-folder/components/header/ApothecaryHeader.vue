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
            url: "/apothecary",
            text: "Товары"
          },
        ]
      }
    }
  }
</script>

<style lang="less">
</style>
