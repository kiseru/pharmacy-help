<template>
  <app-header v-bind:menu-items="menuItems"/>
</template>

<script>
  import AppHeader from "./Header";

  export default {
    name: "DoctorHeader",
    components: {
      AppHeader
    },
    data() {
      return {
        menuItems: [
          {
            url: "/doctor/",
            text: "Cоздать рецепт"
          },
          {
            url: "/doctor/recipes",
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
