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
        ]
      }
    }
  }
</script>

<style lang="less" scoped>

</style>
