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
            url: "/logout",
            text: "Выйти"
          }
        ]
      }
    }
  }
</script>

<style scoped>

</style>