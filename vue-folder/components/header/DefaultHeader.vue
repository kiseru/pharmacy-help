<template>
  <div>
    <apothecary-header v-if="user.role === 'apothecary'"/>
    <doctor-header v-if="user.role === 'doctor'"/>
  </div>
</template>

<script>
  import ApothecaryHeader from "./ApothecaryHeader";
  import DoctorHeader from "./DoctorHeader";

  export default {
    name: "DefaultHeader",
    components: {
      ApothecaryHeader,
      DoctorHeader
    },
    data() {
      return {
        user: null
      };
    },
    beforeMount() {
      this.user = this.$state.getters.getUser();
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

    .navbar-brand {
      margin-left: 16px;
    }
  }
</style>
